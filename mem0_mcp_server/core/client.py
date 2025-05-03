#!/usr/bin/env python
import os
import logging
import traceback
from dotenv import load_dotenv
from mem0 import AsyncMemoryClient

# Global client instance
mem0_instance = None

def initialize_mem0_client():
    """
    Initialize the Mem0 async client.
    
    Returns:
        AsyncMemoryClient or None: The initialized client or None if initialization failed.
    """
    global mem0_instance
    
    # Load environment variables
    logging.info("Searching for .env file...")
    dotenv_path = load_dotenv(override=True)
    if dotenv_path:
        logging.info("Loaded environment variables from default .env path")
    else:
        logging.info(".env file not found or not loaded. Relying on system environment variables.")

    # Check for API key
    api_key = os.getenv("MEM0_API_KEY")
    if not api_key:
        logging.error("MEM0_API_KEY not found in environment variables. Cannot initialize Mem0.")
        return None
    else:
        logging.info("MEM0_API_KEY found in environment.")

    # Initialize Mem0 Instance
    try:
        logging.info("Initializing Mem0 using AsyncMemoryClient...")
        mem0_instance = AsyncMemoryClient(api_key=api_key)
        logging.info("Mem0 Async Client Initialized Successfully.")
        return mem0_instance
    except Exception as e:
        logging.error(f"Failed to initialize Mem0 AsyncMemoryClient: {e}")
        logging.error(traceback.format_exc())
        return None

def get_mem0_client():
    """
    Get the current Mem0 client instance, initializing it if needed.
    
    Returns:
        AsyncMemoryClient or None: The client instance or None if unavailable.
    """
    global mem0_instance
    
    if mem0_instance is None:
        mem0_instance = initialize_mem0_client()
    
    return mem0_instance 