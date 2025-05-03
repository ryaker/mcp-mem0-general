#!/usr/bin/env python
import sys
import logging
import traceback
from fastmcp import FastMCP

# Import from internal modules
from .logging import setup_logging
from .client import initialize_mem0_client

# Global MCP server instance
mcp_server = None

def setup_server(server_name="Mem0 General Memory Server 🧠"):
    """
    Initialize logging, environment, Mem0 client, and FastMCP server.
    
    Args:
        server_name (str, optional): Name of the MCP server. Defaults to "Mem0 General Memory Server 🧠".
        
    Returns:
        FastMCP or None: The initialized FastMCP server or None if setup failed.
    """
    global mcp_server
    
    # Setup logging
    setup_logging()
    logging.info("--- Server Process Started (Setup) ---")
    
    # Initialize Mem0 client
    mem0_client = initialize_mem0_client()
    if not mem0_client:
        logging.error("Failed to initialize Mem0 client, server setup cannot continue.")
        return None
    
    # Initialize FastMCP Server
    try:
        logging.info("Initializing FastMCP Server...")
        mcp_server = FastMCP(server_name)
        logging.info("FastMCP Server Initialized.")
        return mcp_server
    except Exception as e:
        logging.error(f"Failed to initialize FastMCP Server: {e}")
        logging.error(traceback.format_exc())
        return None

def get_mcp_server():
    """
    Get the current MCP server instance, initializing it if needed.
    
    Returns:
        FastMCP or None: The server instance or None if unavailable.
    """
    global mcp_server
    
    if mcp_server is None:
        mcp_server = setup_server()
    
    return mcp_server

def start_server():
    """
    Main entry point to start the MCP server.
    """
    mcp = setup_server()
    
    if not mcp:
        logging.critical("Server setup failed. Exiting.")
        sys.exit(1)
    
    logging.info("Setup complete. Running FastMCP server...")
    
    try:
        mcp.run()
        logging.info("--- Server Process Ended Normally ---")
    except Exception as e:
        logging.critical(f"FastMCP server failed during run: {e}")
        logging.critical(traceback.format_exc())
        sys.exit(1) 