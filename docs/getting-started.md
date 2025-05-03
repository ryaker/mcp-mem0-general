# Getting Started with Mem0 MCP Server

This guide will help you set up and start using the Mem0 MCP Server with your AI assistants.

## Installation

### Prerequisites

Before you begin, ensure you have:

- Python 3.9 or higher installed
- A Mem0.ai account and API key

### Setup Steps

1. **Install the package**:

   ```bash
   pip install mcp-mem0-server
   ```

2. **Configure Cursor or Claude Desktop**:

   For Cursor, add the following to your `~/.cursor/mcp.json` file:
   
   ```json
   "mem0-memory-general": {
     "command": "mcp-mem0-server",
     "args": [],
     "env": {
       "MEM0_API_KEY": "your-mem0-api-key-here"
     }
   }
   ```
   
   For Claude Desktop, add a similar configuration in your settings.

3. **Restart your application**:

   Restart Cursor or Claude Desktop to apply the changes.

## Using the Mem0 MCP Server

Once configured, the Mem0 MCP Server will be automatically available to your AI assistant. No need to manually start a server or connect to a URL.

## Basic Usage Examples

Here are some basic examples to get you started:

### Adding a Memory

```
Add this to my memory using mem0_add_memory: "I prefer dark mode in all applications" with user_id "default_user".
```

### Searching for Memories

```
Search my memories for "preferences" using mem0_search_memory with user_id "default_user".
```

### Retrieving All Memories

```
Show me all my memories using mem0_get_all_memories with user_id "default_user".
```

### Using Specialized Memory Types

```
Add to my episodic memory using mem0_add_episodic_memory: "I visited the Grand Canyon on July 15, 2023" with user_id "default_user".
```

## Next Steps

Now that you have the server configured:

1. Explore the [Complete API Reference](./api-reference.md) to learn about all available tools
2. Check out the [Memory Types Guide](./memory-types.md) to understand different memory structures
3. Learn about [Advanced Features](./advanced-features.md) like custom categories and graph memory

## Troubleshooting

### Common Issues

- **API Key Not Found**: Ensure your Mem0 API key is correctly set in your MCP configuration
- **Tool Not Available**: Restart your application (Cursor or Claude Desktop) after changing configurations
- **Memory Not Found**: Verify you're using the correct user_id in your memory operations (default: "default_user")

### Getting Help

If you encounter issues not covered here:

1. Check the logs (default: `~/.mcp_mem0_server.log`)
2. Review the [API Reference](./api-reference.md) for correct parameter usage
3. Open an issue on our GitHub repository with details about your problem 