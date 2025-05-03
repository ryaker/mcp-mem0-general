#!/usr/bin/env python
import logging
import traceback

from ..core.client import get_mem0_client
from ..core.server import get_mcp_server

def register_specialized_memory_types():
    """Register all specialized memory type operations with the MCP server."""
    mcp = get_mcp_server()
    if not mcp:
        logging.error("Failed to get MCP server instance. Cannot register specialized memory types.")
        return False
        
    # Register all specialized memory type operations
    register_short_term_memory(mcp)
    register_episodic_memory(mcp)
    register_semantic_memory(mcp)
    register_procedural_memory(mcp)
    register_selective_memory(mcp)
    
    logging.info("Registered specialized memory type operations with MCP server")
    return True

def register_short_term_memory(mcp):
    """Register the short-term memory operation with the MCP server."""
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
        mem0_instance = get_mem0_client()
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

def register_episodic_memory(mcp):
    """Register the episodic memory operation with the MCP server."""
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
        mem0_instance = get_mem0_client()
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

def register_semantic_memory(mcp):
    """Register the semantic memory operation with the MCP server."""
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
        mem0_instance = get_mem0_client()
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

def register_procedural_memory(mcp):
    """Register the procedural memory operation with the MCP server."""
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
        mem0_instance = get_mem0_client()
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

def register_selective_memory(mcp):
    """Register the selective memory operation with the MCP server."""
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
        
        mem0_instance = get_mem0_client()
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