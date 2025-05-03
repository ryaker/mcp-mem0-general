#!/usr/bin/env python
import logging
import traceback
import re
from typing import Optional, List, Dict, Any

from ..core.client import get_mem0_client
from ..core.server import get_mcp_server

def register_selective_operations():
    """Register selective memory operations with the MCP server."""
    mcp = get_mcp_server()
    if not mcp:
        logging.error("Failed to get MCP server instance. Cannot register selective memory operations.")
        return False
    
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
        Add a memory with selective pattern matching for including or excluding portions of text.
        
        This tool allows you to control what parts of a text are processed and stored as memories.
        - Use 'includes' to specify regex patterns for text that should be included
        - Use 'excludes' to specify regex patterns for text that should be excluded
        - If both are provided, 'includes' takes precedence (only included text is processed,
          then exclusions are applied to that subset)
        
        Parameters:
            text: The text content to process
            user_id: User identifier for the memory
            includes: Regex pattern for text to include (only matching portions will be stored)
            excludes: Regex pattern for text to exclude (matching portions will be removed)
            metadata: Additional metadata for the memory
            run_id: Session/conversation identifier
            enable_graph: Whether to process the memory for knowledge graph
        """
        logging.info(f"Selective memory add request: user={user_id}, run={run_id}, includes={includes}, excludes={excludes}, enable_graph={enable_graph}")
        logging.info(f"Original text (first 100 chars): {text[:100]}...")
        
        mem0_instance = get_mem0_client()
        if not mem0_instance:
            logging.error("Mem0 instance not initialized.")
            return {"status": "error", "message": "Mem0 instance failed to initialize."}
        
        try:
            # Process text with includes/excludes patterns
            processed_text = apply_selective_patterns(text, includes, excludes)
            
            # Check if we have any text left after filtering
            if not processed_text or processed_text.strip() == "":
                return {
                    "status": "warning",
                    "message": "No text remained after applying filters"
                }
            
            logging.info(f"Processed text (first 100 chars): {processed_text[:100]}...")
            
            # Prepare memory add arguments
            add_args = {
                "user_id": user_id
            }
            
            # Add optional parameters if provided
            if metadata:
                add_args["metadata"] = metadata
            if run_id:
                add_args["run_id"] = run_id
            if enable_graph:
                add_args["enable_graph"] = True
                add_args["output_format"] = "v1.1"
            
            # Always use v2 API for better context
            add_args["version"] = "v2"
            
            # Add the processed memory
            message_list = [{"role": "user", "content": processed_text}]
            response = await mem0_instance.add(message_list, **add_args)
            
            return {
                "status": "success",
                "details": response,
                "original_length": len(text),
                "processed_length": len(processed_text)
            }
            
        except Exception as e:
            logging.error(f"Error in selective memory add: {e}")
            logging.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

def apply_selective_patterns(text: str, includes: str = "", excludes: str = "") -> str:
    """
    Apply selective pattern matching to include or exclude portions of text.
    
    Args:
        text: The original text to process
        includes: Regex pattern for text to include (only matching portions will be kept)
        excludes: Regex pattern for text to exclude (matching portions will be removed)
        
    Returns:
        Processed text after applying patterns
    """
    processed_text = text
    
    try:
        # Handle includes pattern (higher priority)
        if includes:
            try:
                # Find all matches of the includes pattern
                matches = re.finditer(includes, text, re.DOTALL)
                
                # Extract and join all matches
                included_parts = []
                for match in matches:
                    included_parts.append(match.group(0))
                
                if included_parts:
                    processed_text = "\n\n".join(included_parts)
                    logging.info(f"Applied includes pattern, kept {len(included_parts)} matches")
                else:
                    # No matches found, return empty string
                    logging.warning(f"No matches found for includes pattern: {includes}")
                    return ""
                
            except re.error as e:
                logging.error(f"Invalid regex pattern for includes: {e}")
                # Continue with original text if regex is invalid
                processed_text = text
        
        # Handle excludes pattern
        if excludes:
            try:
                # Remove all matches of the excludes pattern
                processed_text = re.sub(excludes, '', processed_text, flags=re.DOTALL)
                logging.info(f"Applied excludes pattern")
                
            except re.error as e:
                logging.error(f"Invalid regex pattern for excludes: {e}")
                # Continue with current processed text if regex is invalid
        
        return processed_text
        
    except Exception as e:
        logging.error(f"Error applying selective patterns: {e}")
        logging.error(traceback.format_exc())
        return text  # Return original text in case of error 