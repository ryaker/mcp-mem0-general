#!/usr/bin/env python
import json
import logging
import traceback

from ..core.client import get_mem0_client
from ..core.server import get_mcp_server

def register_basic_operations():
    """Register all basic memory operations with the MCP server."""
    mcp = get_mcp_server()
    if not mcp:
        logging.error("Failed to get MCP server instance. Cannot register operations.")
        return False
        
    # Register all basic operations
    register_add_memory(mcp)
    register_search_memory(mcp)
    register_get_all_memories(mcp)
    register_get_memory_by_id(mcp)
    register_delete_memory(mcp)
    register_update_memory(mcp)
    
    logging.info("Registered basic memory operations with MCP server")
    return True

def register_add_memory(mcp):
    """Register the add_memory operation with the MCP server."""
    @mcp.tool()
    async def mem0_add_memory(
        text: str,
        user_id: str,
        agent_id: str = "",
        run_id: str = "",
        metadata: dict = {},
        enable_graph: bool = False,
        includes: str = "",
        excludes: str = "",
        timestamp: int = 0,
        expiration_date: str = "",
    ) -> dict:
        """Adds a memory to Mem0. Requires user_id. 
        Parameters like agent_id, run_id, metadata, includes, excludes, timestamp, expiration_date have defaults if not provided.
        Set enable_graph=True to activate graph processing.
        Provide 'includes' or 'excludes' string to filter stored memories.
        Provide 'timestamp' (Unix timestamp integer) to set a custom creation time (default 0 ignored).
        Provide 'expiration_date' (ISO 8601 string) to set an expiration (default "" ignored)."""
        
        logging.info(f"Add request: user={user_id}, agent={agent_id}, run={run_id}, metadata={metadata} (type: {type(metadata)}), enable_graph={enable_graph}, includes='{includes}', excludes='{excludes}', timestamp={timestamp}, expiration_date={expiration_date}, text='{text[:50]}...'") 
        
        mem0_instance = get_mem0_client()
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

            # Apply workaround for other originally optional parameters
            if agent_id:
                add_args["agent_id"] = agent_id
                logging.info(f"Using agent_id: {agent_id}")
            if run_id:
                add_args["run_id"] = run_id
                logging.info(f"Using run_id: {run_id}")
            if timestamp != 0:
                add_args["timestamp"] = timestamp
                logging.info(f"Using custom timestamp: {timestamp}")
            if includes:
                add_args["includes"] = includes
                logging.info(f"Adding 'includes' filter: {includes}")
            if excludes:
                add_args["excludes"] = excludes
                logging.info(f"Adding 'excludes' filter: {excludes}")
            if expiration_date:
                add_args["expiration_date"] = expiration_date
                logging.info(f"Setting expiration date: {expiration_date}")
                
            # Graph handling
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

def register_search_memory(mcp):
    """Register the search_memory operation with the MCP server."""
    @mcp.tool()
    async def mem0_search_memory(
        query: str,
        user_id: str,
        agent_id: str = "",
        run_id: str = "",
        filters: str = "",
        threshold: float = 0.0,
        enable_graph: bool = False,
        memory_duration: str = "",
        memory_type: str = "",
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
        
        mem0_instance = get_mem0_client()
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

            # Apply workaround for other originally optional parameters
            if agent_id:
                search_args["agent_id"] = agent_id
                logging.info(f"Using agent_id: {agent_id}")
            if run_id:
                search_args["run_id"] = run_id
                logging.info(f"Using run_id: {run_id}")
            if threshold != 0.0:
                search_args["threshold"] = threshold
                logging.info(f"Applying threshold: {threshold}")

            # Graph handling
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

def register_get_all_memories(mcp):
    """Register the get_all_memories operation with the MCP server."""
    @mcp.tool()
    async def mem0_get_all_memories(
        user_id: str,
        agent_id: str = "",
        run_id: str = "",
        limit: int = 0,
        page: int = 0,
        page_size: int = 0,
        enable_graph: bool = False,
    ) -> dict:
        """Gets memories from Mem0. Requires user_id.
        Parameters like agent_id, run_id, limit, page, page_size have defaults if not provided.
        Set enable_graph=True to include graph context.
        Use page and page_size for pagination (default 0 ignored).
        Limit is potentially deprecated/conflicts with pagination (default 0 ignored)."""
        
        logging.info(f"Get all request: user={user_id}, agent={agent_id}, run={run_id}, limit={limit}, page={page}, page_size={page_size}, enable_graph={enable_graph}")
        
        mem0_instance = get_mem0_client()
        if not mem0_instance:
            logging.error("Mem0 instance not initialized.")
            return {"status": "error", "message": "Mem0 instance failed to initialize."}
            
        try:
            get_args = {"user_id": user_id}
            
            # Apply workaround for originally optional parameters
            if agent_id:
                get_args["agent_id"] = agent_id
                logging.info(f"Using agent_id: {agent_id}")
            if run_id:
                get_args["run_id"] = run_id
                logging.info(f"Using run_id: {run_id}")
                
            # Pagination and Limit Handling
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
            # Use limit only if provided AND no pagination was provided
            elif limit_provided:
                get_args["limit"] = limit
                logging.info(f"Applying limit: {limit} (Note: Pagination preferred)")
            else:
                logging.info("No pagination or limit provided (or defaults used).")
                
            # Graph handling
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

def register_get_memory_by_id(mcp):
    """Register the get_memory_by_id operation with the MCP server."""
    @mcp.tool()
    async def mem0_get_memory_by_id(memory_id: str) -> dict:
        """Gets a specific memory from Mem0 by its ID."""
        logging.info(f"Get by ID request: memory_id={memory_id}")
        
        mem0_instance = get_mem0_client()
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
                # Handle case where get might return None for not found
                logging.warning(f"Memory not found with ID: {memory_id}")
                return {"status": "error", "message": "Memory not found."}
        except Exception as e:
            logging.error(f"Error getting memory by ID: {e}")
            logging.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

def register_delete_memory(mcp):
    """Register the delete_memory operation with the MCP server."""
    @mcp.tool()
    async def mem0_delete_memory(memory_id: str) -> dict:
        """Deletes a specific memory from Mem0 by its ID."""
        logging.info(f"Delete request: memory_id={memory_id}")
        
        mem0_instance = get_mem0_client()
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

def register_update_memory(mcp):
    """Register the update_memory operation with the MCP server."""
    @mcp.tool()
    async def mem0_update_memory(memory_id: str, data: str) -> dict:
        """Updates a specific memory in Mem0 by its ID."""
        logging.info(f"Update request: memory_id={memory_id}, data='{data[:50]}...'")
        
        mem0_instance = get_mem0_client()
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