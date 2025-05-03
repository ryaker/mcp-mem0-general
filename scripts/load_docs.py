#!/usr/bin/env python
"""
Load Mem0 MCP Server documentation into memory.

This script reads all documentation markdown files and loads them into Mem0
as memories with appropriate metadata for easy retrieval.
"""

import os
import json
import sys
import asyncio
import logging
from pathlib import Path

# Attempt to import Mem0 AsyncMemoryClient
try:
    from mem0 import AsyncMemoryClient
except ImportError:
    print("Error: mem0 package not found. Please install it with 'pip install mem0'")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Default user ID for documentation memories
DEFAULT_USER_ID = "richard_yaker"

# Define special memory IDs
SYSTEM_GUIDE_ID = "76100ac4-896e-488b-90ad-036c0dfaaa80"  # ID of the system guide memory

# Configure paths
DOCS_DIR = Path(__file__).parent.parent / "docs"
README_PATH = Path(__file__).parent.parent / "README.md"

# Mapping of file paths to metadata
FILE_METADATA = {
    "README.md": {"type": "overview", "importance": "high"},
    "docs/README.md": {"type": "documentation_index", "importance": "high"},
    "docs/getting-started.md": {"type": "guide", "topic": "setup", "importance": "high"},
    "docs/api-reference.md": {"type": "reference", "topic": "api", "importance": "high"},
    "docs/memory-types.md": {"type": "guide", "topic": "memory_structure", "importance": "high"},
    "docs/advanced-features.md": {"type": "guide", "topic": "advanced_features", "importance": "high"},
    "docs/configuration.md": {"type": "guide", "topic": "configuration", "importance": "medium"},
    "docs/tutorials/custom-categories.md": {"type": "tutorial", "topic": "custom_categories", "importance": "medium"},
}


async def create_mem0_client():
    """Initialize the Mem0 async client."""
    # Try to get API key from environment
    api_key = os.getenv("MEM0_API_KEY")
    
    if not api_key:
        print("Error: MEM0_API_KEY environment variable not found")
        print("Please set your Mem0 API key with: export MEM0_API_KEY='your-mem0-api-key'")
        sys.exit(1)
    
    try:
        client = AsyncMemoryClient(api_key=api_key)
        logger.info("Mem0 client initialized successfully")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Mem0 client: {e}")
        sys.exit(1)


async def add_memory(client, text, title, file_path, force_update=False):
    """Add a memory with document content."""
    try:
        # Get metadata based on file path
        metadata = FILE_METADATA.get(str(file_path.relative_to(Path(__file__).parent.parent)), {})
        
        # Add title and file path to metadata
        metadata["title"] = title
        metadata["file_path"] = str(file_path.relative_to(Path(__file__).parent.parent))
        
        # Check if this is the main system guide
        memory_id = None
        if file_path.name == "api-reference.md":
            memory_id = SYSTEM_GUIDE_ID
            logger.info(f"Using fixed ID {memory_id} for system guide")
            
        # Add or update the memory
        logger.info(f"Adding memory: {title} (from {file_path.name})")
        
        # Prepare the message format
        message_list = [{"role": "user", "content": text}]
        
        # Add memory arguments
        add_args = {
            "user_id": DEFAULT_USER_ID,
            "metadata": metadata,
            "version": "v2",  # Using v2 API for better context
            "enable_graph": True,  # Enable graph for documentation
        }
        
        # If we have a specific ID and force_update is True, delete and recreate
        if memory_id and force_update:
            try:
                await client.delete(memory_id)
                logger.info(f"Deleted existing memory with ID {memory_id}")
            except Exception as e:
                logger.warning(f"Failed to delete memory {memory_id}: {e}")
            
            add_args["id"] = memory_id
        
        # Add the memory
        response = await client.add(message_list, **add_args)
        
        logger.info(f"Successfully added memory: {title}")
        return response
        
    except Exception as e:
        logger.error(f"Failed to add memory '{title}': {e}")
        return None


async def process_file(client, file_path):
    """Process a single documentation file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Extract title from first line (assuming markdown H1)
        if content.startswith('# '):
            title = content.split('\n')[0].lstrip('# ').strip()
        else:
            title = file_path.stem.replace('-', ' ').title()
        
        # Add memory with the file content
        await add_memory(client, content, title, file_path)
        
    except Exception as e:
        logger.error(f"Failed to process file {file_path}: {e}")


async def process_directory(client, dir_path):
    """Process all markdown files in a directory."""
    logger.info(f"Processing directory: {dir_path}")
    
    for entry in os.scandir(dir_path):
        if entry.is_file() and entry.name.endswith('.md'):
            await process_file(client, Path(entry.path))
        elif entry.is_dir():
            await process_directory(client, Path(entry.path))


async def add_index_memory(client, files_processed):
    """Add a memory that indexes all documentation."""
    index_text = """# Mem0 MCP Server Documentation Index

This memory serves as an index to all documentation loaded into the system.

## Main Sections

1. **Overview** - Basic introduction to the Mem0 MCP Server
2. **Getting Started** - First steps and basic usage instructions  
3. **API Reference** - Detailed information on all available tools
4. **Memory Types** - Understanding different memory structures
5. **Advanced Features** - Exploring enhanced capabilities
6. **Configuration** - Setting up and customizing the server
7. **Tutorials** - Step-by-step guides for specific tasks

## How to Use This Documentation

To access the main system guide with all tools and features:
```
Retrieve memory ID 76100ac4-896e-488b-90ad-036c0dfaaa80 using mem0_get_memory_by_id.
```

To search for specific topics:
```
Search my memories for "[topic]" using mem0_search_memory with user_id "richard_yaker".
```

For example:
```
Search my memories for "custom categories" using mem0_search_memory with user_id "richard_yaker".
```
"""
    
    metadata = {
        "type": "index",
        "topic": "documentation",
        "importance": "critical"
    }
    
    title = "Documentation Index"
    await add_memory(client, index_text, title, Path("docs/index.md"))


async def main():
    """Main entry point for the script."""
    logger.info("Starting documentation loading process")
    
    # Create Mem0 client
    client = await create_mem0_client()
    
    # Counter for processed files
    files_processed = []
    
    # Process the main README
    await process_file(client, README_PATH)
    files_processed.append(README_PATH)
    
    # Process all documentation files
    await process_directory(client, DOCS_DIR)
    
    # Create index memory
    await add_index_memory(client, files_processed)
    
    logger.info("Documentation loading complete")


if __name__ == "__main__":
    asyncio.run(main()) 