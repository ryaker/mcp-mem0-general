#!/usr/bin/env python
import logging
import traceback

from ..core.client import get_mem0_client
from ..core.server import get_mcp_server

def register_short_term_operations():
    """Register short-term memory operations with the MCP server."""
    mcp = get_mcp_server()
    if not mcp:
        logging.error("Failed to get MCP server instance. Cannot register short-term memory operations.")
        return False
    
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
        Add a short-term memory (conversation, working, or attention).
        
        Short-term memories are tied to specific sessions/conversations and are less persistent.
        These memory types are useful for maintaining context within a single interaction session.
        
        Available memory types:
        - conversation: Track content and context of ongoing dialogues
        - working: Hold information being actively processed or manipulated
        - attention: Highlight particularly important information that needs focus
        
        Parameters:
            text: The text content to store
            user_id: User identifier
            run_id: Session/conversation identifier (required for context)
            memory_type: Type of short-term memory ("conversation", "working", "attention")
            metadata: Additional metadata
            enable_graph: Whether to process for knowledge graph
        """
        logging.info(f"Short-term memory add request: user={user_id}, run={run_id}, type={memory_type}, enable_graph={enable_graph}")
        logging.info(f"Text (first 100 chars): {text[:100]}...")
        
        mem0_instance = get_mem0_client()
        if not mem0_instance:
            logging.error("Mem0 instance not initialized.")
            return {"status": "error", "message": "Mem0 instance failed to initialize."}
        
        # Validate memory type
        valid_memory_types = ["conversation", "working", "attention"]
        if memory_type not in valid_memory_types:
            return {
                "status": "error", 
                "message": f"Invalid memory type. Must be one of: {', '.join(valid_memory_types)}"
            }
        
        try:
            # Prepare memory metadata
            if metadata is None:
                metadata = {}
            
            # Ensure metadata is a dictionary
            if not isinstance(metadata, dict):
                logging.warning(f"Metadata is not a dictionary: {metadata}")
                metadata = {}
                
            # Add memory type metadata
            metadata["memory_type"] = memory_type
            metadata["memory_duration"] = "short_term"
            
            # Prepare memory add arguments
            add_args = {
                "user_id": user_id,
                "run_id": run_id,
                "metadata": metadata
            }
            
            # Add graph processing if enabled
            if enable_graph:
                add_args["enable_graph"] = True
                add_args["output_format"] = "v1.1"
            
            # Always use v2 API for better context
            add_args["version"] = "v2"
            
            # Add the memory
            message_list = [{"role": "user", "content": text}]
            response = await mem0_instance.add(message_list, **add_args)
            
            logging.info(f"Added {memory_type} memory for user {user_id}, run {run_id}")
            
            return {
                "status": "success",
                "details": response,
                "memory_type": memory_type
            }
            
        except Exception as e:
            logging.error(f"Error adding short-term memory: {e}")
            logging.error(traceback.format_exc())
            return {"status": "error", "message": str(e)} 