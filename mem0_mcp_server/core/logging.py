#!/usr/bin/env python
import logging
import sys
from pathlib import Path

def setup_logging(log_file=None, log_level=logging.INFO):
    """
    Configure logging for the MCP server.
    
    Args:
        log_file (str, optional): Path to log file. Defaults to None, which uses home directory.
        log_level (int, optional): Logging level. Defaults to logging.INFO.
    """
    # Set default log file in home directory if not specified
    if log_file is None:
        log_file = Path.home() / '.mcp_mem0_server.log'
    elif isinstance(log_file, str):
        log_file = Path(log_file)
    
    # Configure logging format
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stderr)
        ],
    )
    
    # Log initialization
    logging.info("--- Logging initialized ---") 