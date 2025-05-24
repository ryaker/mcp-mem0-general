import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock # Added MagicMock to imports

# Assuming main.py is structured to allow importing of tools
# If not, we might need to adjust the import or the structure of main.py
import src.mcp_mem0_general.main # Import the main module
import pytest_asyncio # Import pytest_asyncio

# Fixture to set up the server and mock mem0_instance
@pytest_asyncio.fixture(scope="function") # Use pytest_asyncio.fixture
async def mock_server_setup():
    # Patch AsyncMemoryClient class within the main module's scope
    # Use MagicMock for the class to ensure its instantiation call is synchronous
    with patch('src.mcp_mem0_general.main.AsyncMemoryClient', new_callable=MagicMock) as MockedAsyncMemoryClientClass: # Corrected patch.MagicMock to MagicMock
        # This is the instance we want main.mem0_instance to become
        mock_mem0_instance_for_test = AsyncMock() 
        mock_mem0_instance_for_test.add = AsyncMock(return_value={"status": "success", "id": "test_id"})
        # When AsyncMemoryClient(...) is called in main.py, it's MockedAsyncMemoryClientClass(...),
        # which will return mock_mem0_instance_for_test.
        MockedAsyncMemoryClientClass.return_value = mock_mem0_instance_for_test

        # Patch os.getenv to ensure MEM0_API_KEY is found by setup_server
        with patch('os.getenv') as mock_getenv:
            mock_getenv.return_value = "fake_api_key"

            # Now, call setup_server().
            # When main.setup_server() executes:
            #   mem0_instance = AsyncMemoryClient(api_key=api_key)
            # it will use our MockedAsyncMemoryClient, which returns mock_mem0_instance.
            # So, src.mcp_mem0_general.main.mem0_instance will be set to mock_mem0_instance.
            if not src.mcp_mem0_general.main.setup_server():
                raise RuntimeError("Test server setup failed: setup_server() returned False")
            
            # The tools defined in setup_server will close over src.mcp_mem0_general.main.mem0_instance,
            # which should now be our mock_mem0_instance_for_test.
            
        yield mock_mem0_instance_for_test # Yield the instance that has the .add method

@pytest.mark.asyncio
async def test_mem0_add_memory_direct_calls_add_with_infer_false(mock_server_setup):
    """
    Tests that mem0_add_memory_direct calls mem0_instance.add with infer=False.
    """
    # mock_server_setup *is* the mocked mem0_instance, thanks to pytest fixture handling.
    # It has also called setup_server() which defines src.mcp_mem0_general.main.mcp.
    mock_add_method = mock_server_setup.add # Use the fixture argument directly

    # mock_server_setup (the fixture) has already run setup_server().
    # src.mcp_mem0_general.main.mem0_instance is now the mock yielded by mock_server_setup.
    # Accessing the tool function via main.mcp._tool_manager._tools[tool_name].fn as per instruction.

    mcp_instance = src.mcp_mem0_general.main.mcp
    if mcp_instance is None:
        raise AssertionError("src.mcp_mem0_general.main.mcp is None after setup_server() call in fixture.")

    # Navigate to the tool function
    tool_manager_attr_name = '_tool_manager'
    if not hasattr(mcp_instance, tool_manager_attr_name):
        raise AttributeError(f"MCP instance does not have '{tool_manager_attr_name}'. Attrs: {dir(mcp_instance)}")
    tool_manager = getattr(mcp_instance, tool_manager_attr_name)

    internal_tools_dict_attr_name = '_tools'
    if not hasattr(tool_manager, internal_tools_dict_attr_name):
        raise AttributeError(f"ToolManager does not have '{internal_tools_dict_attr_name}'. Attrs: {dir(tool_manager)}")
    tools_dict = getattr(tool_manager, internal_tools_dict_attr_name)
    
    if not isinstance(tools_dict, dict):
        raise TypeError(f"ToolManager's '{internal_tools_dict_attr_name}' is not a dict. Type: {type(tools_dict)}")

    tool_function_name = "mem0_add_memory_direct"
    if tool_function_name not in tools_dict:
        raise KeyError(f"Tool '{tool_function_name}' not found in mcp._tool_manager._tools. Keys: {list(tools_dict.keys())}")
    
    tool_object = tools_dict[tool_function_name]

    callable_func_attr_name = 'fn'
    if not hasattr(tool_object, callable_func_attr_name):
        raise AttributeError(f"'Tool' object for '{tool_function_name}' does not have '{callable_func_attr_name}'. Attrs: {dir(tool_object)}")
    
    tool_function = getattr(tool_object, callable_func_attr_name)

    if not callable(tool_function):
         raise TypeError(f"Retrieved tool_object.fn for '{tool_function_name}' is not callable. Type: {type(tool_function)}")

    test_text = "This is a direct memory add."
    test_user_id = "user_123"
    test_agent_id = "agent_abc"
    test_run_id = "run_xyz"
    test_metadata = {"source": "test"}
    
    # Call the tool function obtained from mcp
    await tool_function(
        text=test_text,
        user_id=test_user_id,
        agent_id=test_agent_id,
        run_id=test_run_id,
        metadata=test_metadata,
        # enable_graph, includes, excludes, timestamp, expiration_date use defaults
    )

    # Assert that mem0_instance.add was called once
    mock_add_method.assert_called_once()

    # Get the arguments with which mem0_instance.add was called
    # The first argument to add is message_list, the rest are kwargs
    args, kwargs = mock_add_method.call_args
    
    # Expected message list
    expected_message_list = [{"role": "user", "content": test_text}]
    assert args[0] == expected_message_list, "Message list not as expected"

    # Check for infer=False and other parameters in kwargs
    assert "infer" in kwargs, "infer parameter not found in call to mem0_instance.add"
    assert kwargs["infer"] is False, "infer parameter was not False"
    
    assert kwargs["user_id"] == test_user_id, "user_id not passed correctly"
    assert kwargs["agent_id"] == test_agent_id, "agent_id not passed correctly"
    assert kwargs["run_id"] == test_run_id, "run_id not passed correctly"
    assert kwargs["metadata"] == test_metadata, "metadata not passed correctly"
    assert kwargs["version"] == "v2", "version not passed correctly or default changed"

    # Check other default parameters if necessary, e.g., enable_graph
    # For this test, primarily concerned with 'infer': False
    assert "enable_graph" not in kwargs or kwargs["enable_graph"] is False # Assuming default is False

    # To make this test more robust, we might need to handle the FastMCP instance (mcp)
    # if the tool registration is tightly coupled.
    # However, since we are calling the Python function directly,
    # we primarily need to ensure its internal logic (calling mem0_instance.add) is correct.
    # The fixture's setup_server() call attempts to handle tool registration.
    # If that becomes an issue, we can simplify by not calling setup_server() and
    # just testing the tool function in isolation with a manually patched mem0_instance.
    # The current patch('src.mcp_mem0_general.main.mem0_instance', ...) should cover this.
        # The fixture now ensures setup_server() is called and mem0_instance is correctly mocked.
    
    # Example of how to check if a default parameter was passed as expected
    # if a default value is explicitly set in add_args within the tool
    # (e.g. version="v2" is explicitly set)
    # assert kwargs.get("version") == "v2", "Default version was not v2"
    # assert kwargs.get("output_format") is None, "output_format should not be set if enable_graph is False"

# Example of a simpler fixture if setup_server() is too complex for unit tests:
# @pytest.fixture
# def mock_mem0_instance_global():
#     with patch('src.mcp_mem0_general.main.mem0_instance', new_callable=AsyncMock) as mock_mem0:
#         mock_mem0.add = AsyncMock(return_value={"status": "success", "id": "test_id"})
#         # Directly assign this mock to the main module's global variable
#         # This is necessary because the tool function (mem0_add_memory_direct)
#         # will look up mem0_instance in its own module's global scope.
#         import src.mcp_mem0_general.main
#         src.mcp_mem0_general.main.mem0_instance = mock_mem0
#         yield mock_mem0
#
# @pytest.mark.asyncio
# async def test_mem0_add_memory_direct_simple_mock(mock_mem0_instance_global):
#     mock_add_method = mock_mem0_instance_global.add
#     # ... rest of the test logic ...
#     # tool_function = src.mcp_mem0_general.main.mcp.tools["mem0_add_memory_direct"] # Still need mcp
#     # await tool_function(...) 
#     mock_add_method.assert_called_once()
#     # ... assertions ...

# It's good practice to have an __init__.py in the tests directory
# if it's treated as a package, but for a single file, it might not be strictly necessary
# depending on how pytest discovers tests.
# Creating src/mcp_mem0_general/tests/__init__.py just in case.
# (This would be a separate step if needed)
