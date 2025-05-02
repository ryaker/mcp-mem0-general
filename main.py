#!/usr/bin/env python
import os
import json
import logging
import sys # Import sys for stderr
import traceback
import typing # Add typing import
from pathlib import Path # For home directory
from dotenv import load_dotenv
from fastmcp import FastMCP
# Use AsyncMemoryClient
from mem0 import AsyncMemoryClient 
# Removed MemoryClient and certifi imports

# --- Logging Setup ---
# Log to a file in the user's home directory for better predictability
log_file = Path.home() / '.mcp_mem0_server.log' 
log_format = '%(asctime)s - %(levelname)s - %(message)s'

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[
        logging.FileHandler(log_file), # Log to file in home dir
        logging.StreamHandler(sys.stderr) # Log INFO and above to stderr (visible in terminal)
    ],
    # Force=True might be needed if something else configured logging first
    # force=True 
)

# Separate logger for this module if desired, but basicConfig on root is often enough
# logger = logging.getLogger(__name__)


# Global client variable - now always MemoryClient instance
mem0_instance = None
mcp = None

def setup_server():
    """Initializes logging, environment, basic mem0 client, and FastMCP server."""
    global mem0_instance, mcp

    logging.info("--- Server Process Started (Setup) ---")

    # Load environment variables
    logging.info(f"Searching for .env file...")
    dotenv_path = load_dotenv(override=True)
    if dotenv_path:
        logging.info(f"Loaded environment variables from default .env path")
    else:
        logging.info(".env file not found or not loaded. Relying on system environment variables.")

    # Check for API key
    api_key = os.getenv("MEM0_API_KEY")
    if not api_key:
        logging.error("MEM0_API_KEY not found in environment variables. Cannot initialize Mem0.")
        return False # Indicate setup failure
    else:
        logging.info("MEM0_API_KEY found in environment.")

    # Initialize Mem0 Instance - Use AsyncMemoryClient
    try:
        logging.info("Initializing Mem0 using AsyncMemoryClient...")
        mem0_instance = AsyncMemoryClient(api_key=api_key)
        # Optional: Add an async ping or basic check here if the client supports it
        # Example: await mem0_instance.ping() (if available)
        logging.info("Mem0 Async Client Initialized Successfully.")
    except Exception as e:
        logging.error(f"Failed to initialize Mem0 AsyncMemoryClient: {e}")
        logging.error(traceback.format_exc())
        return False # Indicate setup failure

    # Initialize FastMCP Server
    try:
        logging.info("Initializing FastMCP Server...")
        mcp = FastMCP("Mem0 General Memory Server 🧠")
        logging.info("FastMCP Server Initialized.")
    except Exception as e:
        logging.error(f"Failed to initialize FastMCP Server: {e}")
        logging.error(traceback.format_exc())
        return False # Indicate setup failure

    # --- Define Tools within setup --- 
    # This ensures they are registered with the mcp instance created here
    @mcp.tool()
    async def mem0_add_memory(
        text: str,
        user_id: str,  # Now required
        agent_id: str = "",  # Required with default
        run_id: str = "",  # Required with default
        metadata: dict = {},  # Already fixed: required, defaults to empty dict
        enable_graph: bool = False,
        includes: str = "",  # Required with default
        excludes: str = "",  # Required with default
        timestamp: int = 0,  # Required with default
        expiration_date: str = "",  # Required with default
    ) -> dict:
        """Adds a memory to Mem0. Requires user_id. 
        Parameters like agent_id, run_id, metadata, includes, excludes, timestamp, expiration_date have defaults if not provided.
        Set enable_graph=True to activate graph processing.
        Provide 'includes' or 'excludes' string to filter stored memories.
        Provide 'timestamp' (Unix timestamp integer) to set a custom creation time (default 0 ignored).
        Provide 'expiration_date' (ISO 8601 string) to set an expiration (default "" ignored).""" # Docstring updated
        
        logging.info(f"Add request: user={user_id}, agent={agent_id}, run={run_id}, metadata={metadata} (type: {type(metadata)}), enable_graph={enable_graph}, includes='{includes}', excludes='{excludes}', timestamp={timestamp}, expiration_date={expiration_date}, text='{text[:50]}...'") 
        
        if not mem0_instance:
            logging.error("Mem0 instance not initialized.")
            return {"status": "error", "message": "Mem0 instance failed to initialize."}
        
        try:
            add_args = {"user_id": user_id}
            
            # Add metadata if it's not the default empty dictionary
            if metadata: 
                if isinstance(metadata, dict):
                    add_args["metadata"] = metadata
                    logging.info(f"Adding provided metadata: {metadata}")
                else:
                    logging.warning(f"Received metadata is not a dictionary (type: {type(metadata)}), discarding: {metadata}")
            else:
                logging.info("No metadata provided or metadata is empty, skipping.")

            # --- Apply workaround for other originally optional parameters ---
            if agent_id: # Check if not default ""
                add_args["agent_id"] = agent_id
                logging.info(f"Using agent_id: {agent_id}")
            if run_id: # Check if not default ""
                add_args["run_id"] = run_id
                logging.info(f"Using run_id: {run_id}")
            if timestamp != 0: # Check if not default 0
                add_args["timestamp"] = timestamp
                logging.info(f"Using custom timestamp: {timestamp}")
            if includes: # Check if not default ""
                add_args["includes"] = includes
                logging.info(f"Adding 'includes' filter: {includes}")
            if excludes: # Check if not default ""
                add_args["excludes"] = excludes
                logging.info(f"Adding 'excludes' filter: {excludes}")
            if expiration_date: # Check if not default ""
                add_args["expiration_date"] = expiration_date
                logging.info(f"Setting expiration date: {expiration_date}")
                
            # --- Graph handling ---
            if enable_graph:
                add_args["enable_graph"] = True
                add_args["output_format"] = "v1.1" 
                add_args["version"] = "v2" 
                logging.info(f"Calling mem0_instance.add (GRAPH ENABLED, v2) with args: {add_args}")
            else:
                 add_args["version"] = "v2" 
                 logging.info(f"Calling mem0_instance.add (GRAPH DISABLED, v2) with args: {add_args}")

            message_list = [{"role": "user", "content": text}] 
            response = await mem0_instance.add(message_list, **add_args) 
            
            logging.info(f"Mem0 add response: {response}")
            return {"status": "success", "details": response} 
        except Exception as e:
            logging.error(f"Error adding memory: {e}")
            logging.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def mem0_search_memory(
        query: str,
        user_id: str,  # Now required
        agent_id: str = "",  # Required with default
        run_id: str = "",  # Required with default
        filters: str = "",  # Required with default (JSON string)
        threshold: float = 0.0,  # Required with default
        enable_graph: bool = False,
    ) -> dict:
        """Searches memories in Mem0. Requires user_id and query.
        Parameters like agent_id, run_id, filters, threshold have defaults if not provided.
        Filters is a JSON string representing a dictionary (default "" ignored).
        Threshold is a float for minimum similarity score (default 0.0 ignored).
        Optional: Set enable_graph=True to use graph retrieval.
        Example Filters: '{\\"categories\\": [\\"work\\"], \\"metadata\\": {\\"project\\": \\"xyz\\"}}'"""
        
        logging.info(f"Search request: user={user_id}, agent={agent_id}, run={run_id}, filters={filters}, threshold={threshold}, enable_graph={enable_graph}, query='{query[:50]}...'")
        
        if not mem0_instance:
            logging.error("Mem0 instance not initialized.")
            return {"status": "error", "message": "Mem0 instance failed to initialize."}

        try:
            search_args = {"user_id": user_id}
            filter_dict = None
            
            # Parse filters if provided and not the default empty string
            if filters:
                try:
                    filter_dict = json.loads(filters)
                    if isinstance(filter_dict, dict):
                        search_args["filters"] = filter_dict
                        logging.info(f"Applying parsed filters: {filter_dict}")
                    else:
                        logging.warning(f"Parsed filters is not a dictionary (type: {type(filter_dict)}), discarding filters: {filters}")
                        filter_dict = None # Discard if not dict
                except json.JSONDecodeError as json_err:
                    logging.error(f"Failed to parse filters JSON string: {filters}. Error: {json_err}")
                    # Optionally return an error or proceed without filters
                    # return {"status": "error", "message": f"Invalid filters format: {json_err}"}
                    logging.warning("Proceeding without filters due to parsing error.")
                    filter_dict = None
            else:
                 logging.info("No filters provided or filters is empty, skipping.")

            # --- Apply workaround for other originally optional parameters ---
            if agent_id: # Check if not default ""
                search_args["agent_id"] = agent_id
                logging.info(f"Using agent_id: {agent_id}")
            if run_id: # Check if not default ""
                search_args["run_id"] = run_id
                logging.info(f"Using run_id: {run_id}")
            if threshold != 0.0: # Check if not default 0.0
                search_args["threshold"] = threshold
                logging.info(f"Applying threshold: {threshold}")

            # --- Graph handling ---
            if enable_graph:
                search_args["enable_graph"] = True
                search_args["output_format"] = "v1.1"
                logging.info(f"Calling mem0_instance.search (GRAPH ENABLED) with query='{query}', args={search_args}")
            else:
                 logging.info(f"Calling mem0_instance.search (GRAPH DISABLED) with query='{query}', args={search_args}")

            response = await mem0_instance.search(query, **search_args)
            logging.info(f"Mem0 search response: {response}")
            return {"status": "success", "results": response}
        except Exception as e:
            logging.error(f"Error searching memory: {e}")
            logging.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def mem0_get_all_memories(
        user_id: str,  # Now required
        agent_id: str = "",  # Required with default
        run_id: str = "",  # Required with default
        limit: int = 0,  # Required with default (0 ignored)
        page: int = 0,  # Required with default (0 ignored)
        page_size: int = 0,  # Required with default (0 ignored)
        enable_graph: bool = False,
    ) -> dict:
        """Gets memories from Mem0. Requires user_id.
        Parameters like agent_id, run_id, limit, page, page_size have defaults if not provided.
        Set enable_graph=True to include graph context.
        Use page and page_size for pagination (default 0 ignored).
        Limit is potentially deprecated/conflicts with pagination (default 0 ignored).""" # Updated docstring
        
        logging.info(f"Get all request: user={user_id}, agent={agent_id}, run={run_id}, limit={limit}, page={page}, page_size={page_size}, enable_graph={enable_graph}")
        
        if not mem0_instance:
            logging.error("Mem0 instance not initialized.")
            return {"status": "error", "message": "Mem0 instance failed to initialize."}
            
        try:
            get_args = {"user_id": user_id}  # user_id is now always provided
            
            # --- Apply workaround for originally optional parameters ---
            if agent_id: # Check if not default ""
                get_args["agent_id"] = agent_id
                logging.info(f"Using agent_id: {agent_id}")
            if run_id: # Check if not default ""
                get_args["run_id"] = run_id
                logging.info(f"Using run_id: {run_id}")
                
            # --- Pagination and Limit Handling (checking defaults) ---
            page_provided = (page != 0)
            page_size_provided = (page_size != 0)
            limit_provided = (limit != 0)
            
            # Prefer pagination if page or page_size is explicitly provided (non-zero)
            if page_provided or page_size_provided:
                if page_provided:
                    get_args["page"] = page
                    logging.info(f"Applying pagination: page={page}")
                if page_size_provided:
                    get_args["page_size"] = page_size
                    logging.info(f"Applying pagination: page_size={page_size}")
                if limit_provided:
                    logging.warning("'limit' parameter provided alongside pagination ('page'/'page_size'). Pagination arguments will be used.")
                    # No need to remove limit from get_args as it wasn't added yet
            # Use limit only if provided AND no pagination was provided
            elif limit_provided:
                 get_args["limit"] = limit
                 logging.info(f"Applying limit: {limit} (Note: Pagination preferred)")
            else:
                 logging.info("No pagination or limit provided (or defaults used).")
                 
            # --- Graph handling ---
            if enable_graph:
                get_args["enable_graph"] = True
                get_args["output_format"] = "v1.1"
                logging.info(f"Calling mem0_instance.get_all (GRAPH ENABLED) with args={get_args}")
            else:
                logging.info(f"Calling mem0_instance.get_all (GRAPH DISABLED) with args={get_args}")
                
            response = await mem0_instance.get_all(**get_args)
            logging.info(f"Mem0 get_all response: {response}")
            return {"status": "success", "memories": response}
        except Exception as e:
            logging.error(f"Error getting all memories: {e}")
            logging.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def mem0_get_memory_by_id(memory_id: str) -> dict:
        """Gets a specific memory from Mem0 by its ID."""
        logging.info(f"Get by ID request: memory_id={memory_id}")
        if not mem0_instance:
            logging.error("Mem0 instance not initialized.")
            return {"status": "error", "message": "Mem0 instance failed to initialize."}
        try:
            logging.info(f"Calling mem0_instance.get with memory_id={memory_id}")
            response = await mem0_instance.get(memory_id=memory_id)
            logging.info(f"Mem0 get response: {response}")
            # The get method returns the memory object directly if found, or None/raises error
            if response:
                return {"status": "success", "memory": response}
            else:
                 # Handle case where get might return None for not found, although it might raise error too
                logging.warning(f"Memory not found with ID: {memory_id}")
                return {"status": "error", "message": "Memory not found."}
        except Exception as e:
            # Specific handling for potential not found errors if the API provides them
            # For now, catch generic exception
            logging.error(f"Error getting memory by ID: {e}")
            logging.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def mem0_delete_memory(memory_id: str) -> dict:
        """Deletes a specific memory from Mem0 by its ID."""
        logging.info(f"Delete request: memory_id={memory_id}")
        if not mem0_instance:
            logging.error("Mem0 instance not initialized.")
            return {"status": "error", "message": "Mem0 instance failed to initialize."}
        try:
            logging.info(f"Calling mem0_instance.delete with memory_id={memory_id}")
            response = await mem0_instance.delete(memory_id=memory_id)
            logging.info(f"Mem0 delete response: {response}")
            return {"status": "success", "details": response}
        except Exception as e:
            logging.error(f"Error deleting memory: {e}")
            logging.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def mem0_update_memory(memory_id: str, data: str) -> dict:
        """Updates a specific memory in Mem0 by its ID."""
        logging.info(f"Update request: memory_id={memory_id}, data='{data[:50]}...'")
        if not mem0_instance:
            logging.error("Mem0 instance not initialized.")
            return {"status": "error", "message": "Mem0 instance failed to initialize."}
        try:
            logging.info(f"Calling mem0_instance.update with memory_id={memory_id}, data='{data}'")
            response = await mem0_instance.update(memory_id=memory_id, data=data)
            logging.info(f"Mem0 update response: {response}")
            return {"status": "success", "details": response}
        except Exception as e:
            logging.error(f"Error updating memory: {e}")
            logging.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

    return True # Indicate setup success

def start_server():
    """Main entry point function called by the script."""
    if not setup_server(): # Perform all initialization and check for success
        logging.critical("Server setup failed. Exiting.")
        sys.exit(1) # Exit with error code if setup failed

    logging.info("Setup complete. Running FastMCP server...")
    
    # We already checked mem0_instance and mcp were initialized in setup_server
    # If setup_server returned True, mcp must be valid.
    try:
        mcp.run()
        logging.info("--- Server Process Ended Normally ---")
    except Exception as e:
        logging.critical(f"FastMCP server failed during run: {e}")
        logging.critical(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    start_server() 