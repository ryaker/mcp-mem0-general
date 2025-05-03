# MCP-Mem0-Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Model Context Protocol (MCP) server that provides persistent memory for Large Language Models using Mem0.ai. This server enables LLMs like Claude to maintain persistent memory across conversations.

## Features

- **Persistent Memory Storage**: Store and retrieve memories across LLM conversations
- **Semantic Search**: Find relevant memories using natural language queries
- **Memory Management**: Add, retrieve, update, and delete memories
- **Optional Knowledge Graph Support**: Enable graph-based memory relationships with Neo4j integration
- **Structured Memory Types**: Support for different memory types (short-term, episodic, semantic, procedural)
- **Simple Integration**: Works with any MCP-compatible client like Claude Desktop

## Prerequisites

- Python 3.10 or higher
- Mem0.ai API key ([sign up here](https://mem0.ai))
- (Optional) Neo4j instance for graph features

## Installation

### Using a Virtual Environment (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-mem0-server.git
cd mcp-mem0-server

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install .  # For basic functionality
# OR
pip install .[neo4j]  # If you want to use graph features
```

### Global Installation (Not Recommended)

While global installation is possible, we've encountered dependency conflicts when installing globally alongside other packages. If you must install globally, consider using an isolated environment manager.

## Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```
MEM0_API_KEY=your_mem0_api_key_here
```

For graph features (optional):

```
MEM0_GRAPH_DB_URI=bolt://localhost:7687
MEM0_GRAPH_DB_USER=neo4j
MEM0_GRAPH_DB_PASSWORD=your_password
```

### `.env.example` File

A `.env.example` file is included in the repository. Copy it to create your own `.env` file:

```bash
cp .env.example .env
# Then edit .env with your actual values
```

## Usage

### Running the Server

Once installed, you can run the server using the provided script:

```bash
mcp-mem0-server
```

The server will start and listen for MCP protocol requests.

### Client Configuration

Here's an example configuration for Claude Desktop:

```json
{
  "name": "Memory",
  "description": "Persistent memory with Mem0",
  "command": "/absolute/path/to/mcp-mem0-server",
  "env": {
    "MEM0_API_KEY": "your_mem0_api_key_here"
  }
}
```

> **Note**: Some clients like Claude Desktop may require the absolute path to the executable. You can find this by running `which mcp-mem0-server` in your terminal.

### Available Tools

The server provides these MCP tools:

#### Basic Memory Operations
- `mem0_add_memory`: Add a new memory (generic)
- `mem0_search_memory`: Find memories based on a query
- `mem0_get_all_memories`: Retrieve all stored memories
- `mem0_get_memory_by_id`: Get a specific memory by ID
- `mem0_delete_memory`: Remove a memory
- `mem0_update_memory`: Modify an existing memory

#### Specialized Memory Types
- `mem0_add_short_term_memory`: Add session-specific memory (conversation, working, attention context)
- `mem0_add_episodic_memory`: Add memory of specific events and experiences
- `mem0_add_semantic_memory`: Add memory of facts and preferences
- `mem0_add_procedural_memory`: Add memory of skills and habits

The specialized memory tools provide structured metadata that makes it easier to organize and retrieve memories by type.

## Troubleshooting

### Common Issues

#### "No module named 'fastmcp'"
- Ensure you're using the correct Python environment where the package is installed
- Try running with the full path to the executable

#### TypeError with load_dotenv()
- Make sure you have the latest version installed
- Reinstall the package if needed

#### Command not found
- Check if the script is in your PATH
- Use the absolute path to the script in your client configuration

#### API Key Issues
- Verify your API key is correctly set in the .env file or directly in the client configuration
- Ensure the API key is valid and has the necessary permissions

### Logging

Logs are saved to `~/.mcp_mem0_server.log` and stderr. Check these logs for debugging information.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 