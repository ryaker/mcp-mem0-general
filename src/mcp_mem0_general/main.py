#!/usr/bin/env python
import os
import json
import logging
import sys # Import sys for stderr
import traceback
import typing # Add typing import
from pathlib import Path # For home directory
from dotenv import load_dotenv
# from modelcontextprotocol import FastMCP # Old incorrect import
from mcp.server.fastmcp import FastMCP # Corrected import path
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
        memory_duration: str = "",  # New parameter for filtering by duration type
        memory_type: str = "",  # New parameter for filtering by memory type
    ) -> dict:
        """Searches memories in Mem0. Requires user_id and query.
        Parameters like agent_id, run_id, filters, threshold have defaults if not provided.
        
        For advanced filtering:
        - memory_duration: Filter by "short_term" or "long_term"
        - memory_type: Filter by "conversation", "working", "attention", "episodic", "semantic", or "procedural"
        
        Filters is a JSON string representing a dictionary (default "" ignored).
        Threshold is a float for minimum similarity score (default 0.0 ignored).
        Optional: Set enable_graph=True to use graph retrieval.
        Example Filters: '{\\"categories\\": [\\"work\\"], \\"metadata\\": {\\"project\\": \\"xyz\\"}}'"""
        
        logging.info(f"Search request: user={user_id}, agent={agent_id}, run={run_id}, filters={filters}, memory_duration={memory_duration}, memory_type={memory_type}, threshold={threshold}, enable_graph={enable_graph}, query='{query[:50]}...'")
        
        if not mem0_instance:
            logging.error("Mem0 instance not initialized.")
            return {"status": "error", "message": "Mem0 instance failed to initialize."}

        try:
            search_args = {"user_id": user_id}
            filter_dict = {}
            
            # Parse filters if provided and not the default empty string
            if filters:
                try:
                    parsed_filters = json.loads(filters)
                    if isinstance(parsed_filters, dict):
                        filter_dict.update(parsed_filters)
                        logging.info(f"Applied parsed filters: {parsed_filters}")
                    else:
                        logging.warning(f"Parsed filters is not a dictionary (type: {type(parsed_filters)}), discarding filters: {filters}")
                except json.JSONDecodeError as json_err:
                    logging.error(f"Failed to parse filters JSON string: {filters}. Error: {json_err}")
                    logging.warning("Proceeding without parsed filters due to parsing error.")
            
            # Add memory type filters if provided
            if memory_duration:
                filter_dict["metadata.memory_duration"] = memory_duration
                logging.info(f"Adding memory_duration filter: {memory_duration}")
                
            if memory_type:
                filter_dict["metadata.memory_type"] = memory_type
                logging.info(f"Adding memory_type filter: {memory_type}")
            
            # Only add filters to search args if we have any
            if filter_dict:
                search_args["filters"] = filter_dict
                logging.info(f"Final combined filters: {filter_dict}")

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

    # New specialized memory tools
    @mcp.tool()
    async def mem0_add_short_term_memory(
        text: str,
        user_id: str,
        run_id: str,
        memory_type: str = "conversation",
        metadata: dict = {},
        enable_graph: bool = False,
    ) -> dict:
        """
        Adds short-term memory for real-time context during a session.
        Requires user_id and run_id to create session-specific memory.
        
        memory_type options:
        - "conversation": Recent messages and their order
        - "working": Temporary variables and state
        - "attention": Current focus of the conversation
        """
        if not mem0_instance:
            logging.error("Mem0 instance not initialized.")
            return {"status": "error", "message": "Mem0 instance failed to initialize."}
        
        try:
            # Prepare metadata with memory structure information
            combined_metadata = {
                "memory_duration": "short_term",
                "memory_type": memory_type
            }
            
            # Merge with any user-provided metadata
            if metadata:
                combined_metadata.update(metadata)
                
            logging.info(f"Adding short-term memory: type={memory_type}, user={user_id}, run={run_id}")
            
            add_args = {
                "user_id": user_id,
                "run_id": run_id,
                "metadata": combined_metadata,
                "version": "v2"
            }
            
            if enable_graph:
                add_args["enable_graph"] = True
                add_args["output_format"] = "v1.1"
                
            message_list = [{"role": "user", "content": text}]
            response = await mem0_instance.add(message_list, **add_args)
            
            logging.info(f"Mem0 add short-term memory response: {response}")
            return {"status": "success", "details": response}
        except Exception as e:
            logging.error(f"Error adding short-term memory: {e}")
            logging.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}
    
    @mcp.tool()
    async def mem0_add_episodic_memory(
        text: str,
        user_id: str,
        event_date: str = "",
        metadata: dict = {},
        enable_graph: bool = False,
    ) -> dict:
        """
        Adds episodic memory - remembers specific events and experiences.
        Requires user_id to create persistent memory.
        
        Optionally provide:
        - event_date: When this event occurred (e.g., "2023-05-15")
        - metadata: Additional structured data about this memory
        - enable_graph: Enable knowledge graph processing
        """
        if not mem0_instance:
            logging.error("Mem0 instance not initialized.")
            return {"status": "error", "message": "Mem0 instance failed to initialize."}
        
        try:
            # Prepare metadata with memory structure information
            combined_metadata = {
                "memory_duration": "long_term",
                "memory_type": "episodic"
            }
            
            # Add event date if provided
            if event_date:
                combined_metadata["event_date"] = event_date
                
            # Merge with any user-provided metadata
            if metadata:
                combined_metadata.update(metadata)
                
            logging.info(f"Adding episodic memory for user={user_id}")
            
            add_args = {
                "user_id": user_id,
                "metadata": combined_metadata,
                "version": "v2"
            }
            
            if enable_graph:
                add_args["enable_graph"] = True
                add_args["output_format"] = "v1.1"
                
            message_list = [{"role": "user", "content": text}]
            response = await mem0_instance.add(message_list, **add_args)
            
            logging.info(f"Mem0 add episodic memory response: {response}")
            return {"status": "success", "details": response}
        except Exception as e:
            logging.error(f"Error adding episodic memory: {e}")
            logging.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}
    
    @mcp.tool()
    async def mem0_add_semantic_memory(
        text: str,
        user_id: str,
        category: str = "",
        metadata: dict = {},
        enable_graph: bool = True,
    ) -> dict:
        """
        Adds semantic memory - stores facts and preferences.
        Requires user_id to create persistent memory.
        
        Optionally provide:
        - category: Type of fact (e.g., "preference", "personal_info", "knowledge")
        - metadata: Additional structured data about this memory
        - enable_graph: Enable knowledge graph processing (default: True for semantic memories)
        """
        if not mem0_instance:
            logging.error("Mem0 instance not initialized.")
            return {"status": "error", "message": "Mem0 instance failed to initialize."}
        
        try:
            # Prepare metadata with memory structure information
            combined_metadata = {
                "memory_duration": "long_term",
                "memory_type": "semantic"
            }
            
            # Add category if provided
            if category:
                combined_metadata["category"] = category
                
            # Merge with any user-provided metadata
            if metadata:
                combined_metadata.update(metadata)
                
            logging.info(f"Adding semantic memory for user={user_id}, category={category}")
            
            add_args = {
                "user_id": user_id,
                "metadata": combined_metadata,
                "version": "v2"
            }
            
            # Default to enable_graph=True for semantic memories unless explicitly disabled
            if enable_graph:
                add_args["enable_graph"] = True
                add_args["output_format"] = "v1.1"
                
            message_list = [{"role": "user", "content": text}]
            response = await mem0_instance.add(message_list, **add_args)
            
            logging.info(f"Mem0 add semantic memory response: {response}")
            return {"status": "success", "details": response}
        except Exception as e:
            logging.error(f"Error adding semantic memory: {e}")
            logging.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}
    
    @mcp.tool()
    async def mem0_add_procedural_memory(
        text: str,
        user_id: str,
        skill_area: str = "",
        metadata: dict = {},
        enable_graph: bool = False,
    ) -> dict:
        """
        Adds procedural memory - records skills and habits.
        Requires user_id to create persistent memory.
        
        Optionally provide:
        - skill_area: Area of skill/habit (e.g., "coding", "communication", "workflow")
        - metadata: Additional structured data about this memory
        - enable_graph: Enable knowledge graph processing
        """
        if not mem0_instance:
            logging.error("Mem0 instance not initialized.")
            return {"status": "error", "message": "Mem0 instance failed to initialize."}
        
        try:
            # Prepare metadata with memory structure information
            combined_metadata = {
                "memory_duration": "long_term",
                "memory_type": "procedural"
            }
            
            # Add skill area if provided
            if skill_area:
                combined_metadata["skill_area"] = skill_area
                
            # Merge with any user-provided metadata
            if metadata:
                combined_metadata.update(metadata)
                
            logging.info(f"Adding procedural memory for user={user_id}, skill_area={skill_area}")
            
            add_args = {
                "user_id": user_id,
                "metadata": combined_metadata,
                "version": "v2"
            }
            
            if enable_graph:
                add_args["enable_graph"] = True
                add_args["output_format"] = "v1.1"
                
            message_list = [{"role": "user", "content": text}]
            response = await mem0_instance.add(message_list, **add_args)
            
            logging.info(f"Mem0 add procedural memory response: {response}")
            return {"status": "success", "details": response}
        except Exception as e:
            logging.error(f"Error adding procedural memory: {e}")
            logging.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def mem0_update_categories(
        custom_categories: list,
        explanation: str = "",
    ) -> dict:
        """
        Update the project's custom memory categories.
        
        Provide a list of custom categories as dictionaries with category name as key and description as value.
        These categories will be used instead of the default ones (personal_details, family, etc.).
        
        Example:
        [
            {"coding_patterns": "Programming style preferences and development habits"},
            {"app_settings": "User interface preferences and configuration choices"},
            {"learning_goals": "Educational objectives and skill development targets"}
        ]
        
        Optionally provide an explanation to document the reason for these categories.
        """
        logging.info(f"Updating custom categories: {custom_categories}")
        
        if not mem0_instance:
            logging.error("Mem0 instance not initialized.")
            return {"status": "error", "message": "Mem0 instance failed to initialize."}
        
        try:
            response = await mem0_instance.update_project(custom_categories=custom_categories)
            logging.info(f"Updated custom categories: {response}")
            return {
                "status": "success", 
                "details": response,
                "explanation": explanation if explanation else "Custom categories updated successfully"
            }
        except Exception as e:
            logging.error(f"Error updating custom categories: {e}")
            logging.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def mem0_get_categories(
    ) -> dict:
        """
        Get the current custom categories for the project.
        
        Returns the list of custom categories if defined, or indicates that default categories 
        are being used (personal_details, family, professional_details, sports, travel, etc.)
        """
        logging.info("Getting current custom categories")
        
        if not mem0_instance:
            logging.error("Mem0 instance not initialized.")
            return {"status": "error", "message": "Mem0 instance failed to initialize."}
        
        try:
            response = await mem0_instance.get_project(fields=["custom_categories"])
            logging.info(f"Retrieved custom categories: {response}")
            
            if response.get("custom_categories"):
                return {
                    "status": "success", 
                    "custom_categories": response.get("custom_categories"),
                    "using_default": False
                }
            else:
                return {
                    "status": "success", 
                    "custom_categories": None,
                    "using_default": True,
                    "default_categories": [
                        "personal_details", "family", "professional_details", 
                        "sports", "travel", "food", "music", "health", 
                        "technology", "hobbies", "fashion", "entertainment", 
                        "milestones", "user_preferences", "misc"
                    ]
                }
        except Exception as e:
            logging.error(f"Error getting custom categories: {e}")
            logging.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def mem0_set_instructions(
        instructions: str,
        explanation: str = "",
    ) -> dict:
        """
        Set custom instructions for memory extraction.
        
        These instructions guide how information is extracted and stored from conversations.
        They act as project-level guidelines for memory processing.
        
        Example:
        "Extract only technical information about coding preferences. 
         Ignore personal details and focus on tools, languages and frameworks.
         Always capture specific version numbers and library preferences."
         
        Optionally provide an explanation to document the purpose of these instructions.
        """
        logging.info(f"Setting custom instructions: {instructions[:100]}...")
        
        if not mem0_instance:
            logging.error("Mem0 instance not initialized.")
            return {"status": "error", "message": "Mem0 instance failed to initialize."}
        
        try:
            response = await mem0_instance.update_project(custom_instructions=instructions)
            logging.info(f"Set custom instructions: {response}")
            return {
                "status": "success", 
                "details": response,
                "explanation": explanation if explanation else "Custom instructions set successfully"
            }
        except Exception as e:
            logging.error(f"Error setting custom instructions: {e}")
            logging.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def mem0_get_instructions(
    ) -> dict:
        """
        Get the current custom instructions for the project.
        
        Returns the custom instructions if defined, or indicates that no custom
        instructions are being used.
        """
        logging.info("Getting current custom instructions")
        
        if not mem0_instance:
            logging.error("Mem0 instance not initialized.")
            return {"status": "error", "message": "Mem0 instance failed to initialize."}
        
        try:
            response = await mem0_instance.get_project(fields=["custom_instructions"])
            logging.info(f"Retrieved custom instructions: {response}")
            
            return {
                "status": "success", 
                "custom_instructions": response.get("custom_instructions"),
                "has_custom_instructions": bool(response.get("custom_instructions"))
            }
        except Exception as e:
            logging.error(f"Error getting custom instructions: {e}")
            logging.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def mem0_get_graph_relations(
        user_id: str,
        entity: str,
        relation_type: str = "",
    ) -> dict:
        """
        Get graph relationships for a specific entity.
        Requires graph features to be enabled.
        
        Parameters:
        - user_id: User ID to query relationships for
        - entity: The entity to find relationships for (e.g., "Python", "Machine Learning")
        - relation_type: Optional filter for specific relation types
        
        Returns graph relationships connected to the entity, such as:
        - "Python" -> "is used for" -> "Web Development"
        - "Python" -> "has library" -> "TensorFlow"
        """
        logging.info(f"Getting graph relations for entity: {entity}, user: {user_id}")
        
        if not mem0_instance:
            logging.error("Mem0 instance not initialized.")
            return {"status": "error", "message": "Mem0 instance failed to initialize."}
        
        try:
            # Implementation depends on Mem0's graph API, this is a provisional approach
            search_args = {
                "user_id": user_id,
                "enable_graph": True,
                "output_format": "v1.1",
                "filters": {"entity": entity}
            }
            
            if relation_type:
                search_args["filters"]["relation_type"] = relation_type
            
            # Use search with entity as query and graph enabled
            response = await mem0_instance.search(
                entity, 
                **search_args
            )
            
            logging.info(f"Retrieved graph relations: {response}")
            return {
                "status": "success", 
                "entity": entity,
                "relations": response
            }
        except Exception as e:
            logging.error(f"Error getting graph relations: {e}")
            logging.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def mem0_send_feedback(
        memory_id: str,
        feedback_type: str,
        comments: str = "",
    ) -> dict:
        """
        Provide feedback on a memory to improve future retrieval quality.
        
        Parameters:
        - memory_id: ID of the memory to provide feedback on
        - feedback_type: Type of feedback (choose one):
          * "relevant" - The memory was relevant to the query
          * "not_relevant" - The memory wasn't relevant to the query
          * "accurate" - The memory contained accurate information
          * "inaccurate" - The memory contained inaccurate information
        - comments: Optional additional feedback comments
        
        This feedback helps the system improve memory quality and retrieval accuracy over time.
        """
        valid_feedback_types = ["relevant", "not_relevant", "accurate", "inaccurate"]
        
        if feedback_type not in valid_feedback_types:
            return {
                "status": "error", 
                "message": f"Invalid feedback type. Must be one of: {', '.join(valid_feedback_types)}"
            }
        
        logging.info(f"Sending feedback for memory: {memory_id}, type: {feedback_type}")
        
        if not mem0_instance:
            logging.error("Mem0 instance not initialized.")
            return {"status": "error", "message": "Mem0 instance failed to initialize."}
        
        try:
            # Implementation based on Mem0's feedback API
            response = await mem0_instance.feedback(
                memory_id=memory_id,
                feedback_type=feedback_type,
                comments=comments
            )
            
            logging.info(f"Sent feedback successfully: {response}")
            return {
                "status": "success", 
                "details": response
            }
        except Exception as e:
            logging.error(f"Error sending feedback: {e}")
            logging.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

    # Enhance the existing mem0_add_memory function with more documentation on includes/excludes
    @mcp.tool()
    async def mem0_add_memory_selective(
        text: str,
        user_id: str,
        includes: str = "",
        excludes: str = "",
        metadata: dict = {},
        run_id: str = "",
        enable_graph: bool = False,
    ) -> dict:
        """
        Adds a memory to Mem0 with selective memory controls.
        
        Parameters:
        - text: The content to store as a memory
        - user_id: User ID to associate the memory with
        - includes: Specific types of information to include (e.g., "only work-related information")
          Use this to focus memory on specific topics or information types
        - excludes: Types of information to exclude (e.g., "ignore personal details")
          Use this to prevent storing sensitive or irrelevant information
        - metadata: Additional structured data about this memory
        - run_id: Optional session identifier for conversation context
        - enable_graph: Enable knowledge graph processing
        
        Examples:
        - includes="only remember hobby-related information"
        - excludes="ignore addresses and phone numbers"
        
        This provides more control over what information gets stored in memory.
        """
        logging.info(f"Adding selective memory: user={user_id}, run={run_id}, includes='{includes}', excludes='{excludes}', text='{text[:50]}...'")
        
        if not mem0_instance:
            logging.error("Mem0 instance not initialized.")
            return {"status": "error", "message": "Mem0 instance failed to initialize."}
        
        try:
            add_args = {"user_id": user_id, "version": "v2"}
            
            # Add metadata if provided
            if metadata and isinstance(metadata, dict):
                add_args["metadata"] = metadata
                logging.info(f"Using provided metadata: {metadata}")
            
            # Add selective memory parameters
            if includes:
                add_args["includes"] = includes
                logging.info(f"Using includes filter: '{includes}'")
            
            if excludes:
                add_args["excludes"] = excludes
                logging.info(f"Using excludes filter: '{excludes}'")
            
            # Add run_id if provided
            if run_id:
                add_args["run_id"] = run_id
                logging.info(f"Using run_id: {run_id}")
            
            # Add graph processing if enabled
            if enable_graph:
                add_args["enable_graph"] = True
                add_args["output_format"] = "v1.1"
                logging.info(f"Enabling graph processing")
            
            message_list = [{"role": "user", "content": text}]
            response = await mem0_instance.add(message_list, **add_args)
            
            logging.info(f"Mem0 add selective memory response: {response}")
            return {"status": "success", "details": response}
        except Exception as e:
            logging.error(f"Error adding selective memory: {e}")
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