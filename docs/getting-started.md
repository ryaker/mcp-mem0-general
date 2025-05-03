# Getting Started with Mem0 MCP Server

This guide will help you set up and start using the Mem0 MCP Server with your AI assistants.

## Installation

### Prerequisites

Before you begin, ensure you have:

- Python 3.9 or higher installed
- A Mem0.ai account and API key
- [Optional] Neo4j installed (for graph features)

### Setup Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/mcp-mem0-general.git
   cd mcp-mem0-general
   ```

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the server**:

   Copy the sample configuration file:
   ```bash
   cp mcp-config.sample.json mcp-config.json
   ```

   Edit `mcp-config.json` to add your Mem0 API key and customize other settings.

   Alternatively, you can set the API key as an environment variable:
   ```bash
   export MEM0_API_KEY="your-mem0-api-key"
   ```

## Starting the Server

Run the server using the following command:

```bash
python main.py
```

By default, the server will start on `http://localhost:8000`.

## Connecting to the Server

### In Claude Desktop or Other MCP Clients

1. Open your MCP-compatible client (e.g., Claude Desktop)
2. Go to settings and add a new MCP server with the URL: `http://localhost:8000`
3. Give your server a name (e.g., "Mem0 Memory")
4. Save the settings and restart the client if necessary

### In Custom Applications

If you're building your own client application:

1. Configure your client to connect to `http://localhost:8000`
2. Set up the client to request the MCP server's tool list
3. Implement calls to the Mem0 tools in your application

## Basic Usage Examples

Here are some basic examples to get you started:

### Adding a Memory

```
Add this to my memory using mem0_add_memory: "I prefer dark mode in all applications" with user_id "your-user-id".
```

### Searching for Memories

```
Search my memories for "preferences" using mem0_search_memory with user_id "your-user-id".
```

### Retrieving All Memories

```
Show me all my memories using mem0_get_all_memories with user_id "your-user-id".
```

### Using Specialized Memory Types

```
Add to my episodic memory using mem0_add_episodic_memory: "I visited the Grand Canyon on July 15, 2023" with user_id "your-user-id".
```

## Next Steps

Now that you have the server running and connected:

1. Explore the [Complete API Reference](./api-reference.md) to learn about all available tools
2. Check out the [Memory Types Guide](./memory-types.md) to understand different memory structures
3. Try some of our [Tutorials](./tutorials/) for step-by-step guides on specific use cases
4. Learn about [Advanced Features](./advanced-features.md) like custom categories and graph memory

## Troubleshooting

### Common Issues

- **API Key Not Found**: Ensure your Mem0 API key is correctly set in `mcp-config.json` or as an environment variable
- **Port Already in Use**: If port 8000 is already being used, modify the port in the configuration
- **Connection Refused**: Make sure the server is running and your client is configured with the correct URL
- **Memory Not Found**: Verify you're using the correct user_id in your memory operations

### Getting Help

If you encounter issues not covered here:

1. Check the server logs (default: `~/.mcp_mem0_server.log`)
2. Review the [API Reference](./api-reference.md) for correct parameter usage
3. Open an issue on our GitHub repository with details about your problem 