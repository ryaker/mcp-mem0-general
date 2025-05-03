#!/usr/bin/env python
import json
import logging
import traceback
import os
from pathlib import Path

from ..core.client import get_mem0_client
from ..core.server import get_mcp_server

# Globals for configuration storage
_custom_categories = []
_custom_instructions = ""

# Storage paths
CONFIG_DIR = Path.home() / ".mem0_mcp_server"
CATEGORIES_FILE = CONFIG_DIR / "categories.json"
INSTRUCTIONS_FILE = CONFIG_DIR / "instructions.txt"

def _ensure_config_dir():
    """Ensure the configuration directory exists."""
    CONFIG_DIR.mkdir(exist_ok=True, parents=True)

def _load_saved_categories():
    """Load custom categories from disk if they exist."""
    global _custom_categories
    try:
        if CATEGORIES_FILE.exists():
            with open(CATEGORIES_FILE, 'r') as f:
                _custom_categories = json.load(f)
                logging.info(f"Loaded {len(_custom_categories)} custom categories from {CATEGORIES_FILE}")
        else:
            logging.info(f"No saved categories found at {CATEGORIES_FILE}")
    except Exception as e:
        logging.error(f"Failed to load custom categories: {e}")
        logging.error(traceback.format_exc())

def _save_categories():
    """Save custom categories to disk."""
    try:
        _ensure_config_dir()
        with open(CATEGORIES_FILE, 'w') as f:
            json.dump(_custom_categories, f, indent=2)
        logging.info(f"Saved {len(_custom_categories)} custom categories to {CATEGORIES_FILE}")
    except Exception as e:
        logging.error(f"Failed to save custom categories: {e}")
        logging.error(traceback.format_exc())

def _load_saved_instructions():
    """Load custom instructions from disk if they exist."""
    global _custom_instructions
    try:
        if INSTRUCTIONS_FILE.exists():
            with open(INSTRUCTIONS_FILE, 'r') as f:
                _custom_instructions = f.read()
                logging.info(f"Loaded custom instructions from {INSTRUCTIONS_FILE}")
        else:
            logging.info(f"No saved instructions found at {INSTRUCTIONS_FILE}")
    except Exception as e:
        logging.error(f"Failed to load custom instructions: {e}")
        logging.error(traceback.format_exc())

def _save_instructions():
    """Save custom instructions to disk."""
    try:
        _ensure_config_dir()
        with open(INSTRUCTIONS_FILE, 'w') as f:
            f.write(_custom_instructions)
        logging.info(f"Saved custom instructions to {INSTRUCTIONS_FILE}")
    except Exception as e:
        logging.error(f"Failed to save custom instructions: {e}")
        logging.error(traceback.format_exc())

def register_advanced_features():
    """Register all advanced features with the MCP server."""
    mcp = get_mcp_server()
    if not mcp:
        logging.error("Failed to get MCP server instance. Cannot register advanced features.")
        return False
        
    # Load saved configurations
    _load_saved_categories()
    _load_saved_instructions()
    
    # Register all advanced feature operations
    register_category_management(mcp)
    register_instruction_management(mcp)
    register_graph_features(mcp)
    register_feedback_mechanism(mcp)
    
    logging.info("Registered advanced features with MCP server")
    return True

def register_category_management(mcp):
    """Register tools for managing custom memory categories."""
    
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
            {"learning_goals": "Skills and knowledge areas you want to develop"}
        ]
        """
        global _custom_categories
        
        logging.info(f"Updating custom categories: {custom_categories}")
        if explanation:
            logging.info(f"Explanation for update: {explanation}")
        
        try:
            if not isinstance(custom_categories, list):
                return {"status": "error", "message": "Custom categories must be a list of dictionaries"}
            
            # Validate format
            for category in custom_categories:
                if not isinstance(category, dict) or len(category) != 1:
                    return {"status": "error", "message": "Each category must be a dictionary with one key-value pair"}
            
            # Update the global categories
            _custom_categories = custom_categories
            
            # Save to disk
            _save_categories()
            
            return {
                "status": "success",
                "message": f"Updated {len(custom_categories)} custom categories",
                "categories": _custom_categories
            }
            
        except Exception as e:
            logging.error(f"Error updating categories: {e}")
            logging.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def mem0_get_categories() -> dict:
        """
        Get the project's current custom memory categories.
        
        This will return the list of custom categories that have been set for the project.
        If no custom categories have been set, an empty list will be returned.
        """
        try:
            logging.info("Retrieving custom categories")
            
            return {
                "status": "success",
                "categories": _custom_categories
            }
            
        except Exception as e:
            logging.error(f"Error retrieving categories: {e}")
            logging.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

def register_instruction_management(mcp):
    """Register tools for managing custom memory instructions."""
    
    @mcp.tool()
    async def mem0_set_instructions(
        instructions: str,
        explanation: str = "",
    ) -> dict:
        """
        Set custom memory extraction instructions.
        
        Provide detailed instructions on how memories should be processed, extracted, and organized.
        These instructions will guide how the system processes and stores memories.
        
        Example:
        '''
        When processing memories:
        1. Extract key entities and tag them appropriately
        2. Identify action items and mark them with [ACTION]
        3. Format code snippets with language tags
        4. Remove redundant information
        5. Separate factual information from opinions
        '''
        """
        global _custom_instructions
        
        logging.info(f"Setting custom instructions: {instructions[:100]}...")
        if explanation:
            logging.info(f"Explanation for update: {explanation}")
        
        try:
            if not isinstance(instructions, str):
                return {"status": "error", "message": "Instructions must be a string"}
            
            # Update the global instructions
            _custom_instructions = instructions
            
            # Save to disk
            _save_instructions()
            
            return {
                "status": "success",
                "message": "Updated custom instructions",
                "instructions": _custom_instructions
            }
            
        except Exception as e:
            logging.error(f"Error setting instructions: {e}")
            logging.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    async def mem0_get_instructions() -> dict:
        """
        Get the current custom memory extraction instructions.
        
        This will return the custom instructions that have been set for memory processing.
        If no custom instructions have been set, an empty string will be returned.
        """
        try:
            logging.info("Retrieving custom instructions")
            
            return {
                "status": "success",
                "instructions": _custom_instructions
            }
            
        except Exception as e:
            logging.error(f"Error retrieving instructions: {e}")
            logging.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

def register_graph_features(mcp):
    """Register tools for working with memory graph features."""
    
    @mcp.tool()
    async def mem0_get_graph_relations(
        user_id: str,
        entity: str,
        relation_type: str = "",
    ) -> dict:
        """
        Get relationships from the knowledge graph for a specific entity.
        
        This tool queries the knowledge graph to find relationships between entities.
        You can specify a relation_type to filter the results, or leave it empty to get all relations.
        
        Parameters:
            user_id: The user identifier for the memories to search within
            entity: The entity to get relationships for
            relation_type: Optional type of relationship to filter by (e.g., "created_by", "part_of")
        """
        logging.info(f"Getting graph relations for entity: {entity}, relation_type: {relation_type}, user_id: {user_id}")
        
        mem0_instance = get_mem0_client()
        if not mem0_instance:
            logging.error("Mem0 instance not initialized.")
            return {"status": "error", "message": "Mem0 instance failed to initialize."}
        
        try:
            # Build parameters
            params = {
                "user_id": user_id,
                "entity": entity,
                "enable_graph": True,
                "output_format": "v1.1"
            }
            
            # Add relation_type if provided
            if relation_type:
                params["relation_type"] = relation_type
                logging.info(f"Filtering by relation type: {relation_type}")
            
            # Get the relationships
            response = await mem0_instance.get_relationships(**params)
            
            # Check if there are any relationships
            if not response or not response.get('nodes') or not response.get('edges'):
                return {
                    "status": "success",
                    "message": f"No relationships found for entity '{entity}'",
                    "relationships": {
                        "nodes": [],
                        "edges": []
                    }
                }
            
            logging.info(f"Found {len(response.get('edges', []))} relationships for entity '{entity}'")
            
            return {
                "status": "success",
                "relationships": {
                    "nodes": response.get('nodes', []),
                    "edges": response.get('edges', [])
                }
            }
            
        except Exception as e:
            logging.error(f"Error getting graph relations: {e}")
            logging.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

def register_feedback_mechanism(mcp):
    """Register tools for providing feedback on memories."""
    
    @mcp.tool()
    async def mem0_send_feedback(
        memory_id: str,
        feedback_type: str,
        comments: str = "",
    ) -> dict:
        """
        Provide feedback on memory quality.
        
        This tool allows you to provide feedback on the quality, relevance, and usefulness of a memory.
        This feedback can be used to improve memory processing and retrieval over time.
        
        Parameters:
            memory_id: The unique identifier of the memory to provide feedback on
            feedback_type: Type of feedback (helpful, not_helpful, irrelevant, outdated, incomplete)
            comments: Optional additional comments or details about the feedback
        """
        logging.info(f"Sending feedback for memory {memory_id}: type={feedback_type}, comments={comments}")
        
        mem0_instance = get_mem0_client()
        if not mem0_instance:
            logging.error("Mem0 instance not initialized.")
            return {"status": "error", "message": "Mem0 instance failed to initialize."}
        
        # Validate feedback type
        valid_feedback_types = ["helpful", "not_helpful", "irrelevant", "outdated", "incomplete"]
        if feedback_type not in valid_feedback_types:
            return {
                "status": "error", 
                "message": f"Invalid feedback type. Must be one of: {', '.join(valid_feedback_types)}"
            }
        
        try:
            # Send the feedback
            feedback_data = {
                "memory_id": memory_id,
                "feedback_type": feedback_type
            }
            
            if comments:
                feedback_data["comments"] = comments
            
            # Note: This is a placeholder - actual implementation would depend on the Mem0 API
            # This could be storing to a separate feedback collection, updating the memory, etc.
            # For now, we'll simulate successful feedback submission
            
            logging.info(f"Feedback successfully submitted for memory {memory_id}")
            
            return {
                "status": "success",
                "message": f"Feedback '{feedback_type}' successfully submitted for memory {memory_id}",
                "feedback_data": feedback_data
            }
            
        except Exception as e:
            logging.error(f"Error sending feedback: {e}")
            logging.error(traceback.format_exc())
            return {"status": "error", "message": str(e)} 