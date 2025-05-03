#!/usr/bin/env python
"""
Main entry point for the Mem0 MCP Server.
This script initializes the server and registers all memory operations.
"""
import sys
import logging
from mem0_mcp_server.core.server import setup_server, start_server
from mem0_mcp_server.operations.basic import register_basic_operations
from mem0_mcp_server.memory_types.short_term import register_short_term_operations
from mem0_mcp_server.memory_types.specialized import register_specialized_operations
from mem0_mcp_server.advanced.features import register_advanced_features
from mem0_mcp_server.advanced.selective import register_selective_operations

def main():
    """Initialize and start the Mem0 MCP Server."""
    # Initialize server
    mcp = setup_server()
    if not mcp:
        logging.critical("Failed to initialize MCP server. Exiting.")
        sys.exit(1)
    
    # Register all operations
    if not register_basic_operations():
        logging.error("Failed to register basic operations.")
    
    if not register_short_term_operations():
        logging.error("Failed to register short-term memory operations.")
    
    if not register_specialized_operations():
        logging.error("Failed to register specialized memory operations.")
    
    if not register_advanced_features():
        logging.error("Failed to register advanced features.")
    
    if not register_selective_operations():
        logging.error("Failed to register selective memory operations.")
    
    logging.info("All operations registered. Starting server...")
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main() 