# Mem0 MCP Server

A Model Context Protocol (MCP) server for integrating AI assistants with Mem0.ai's persistent memory system.

## Overview

This server provides MCP-compatible tools that let any compatible AI assistant access and manage persistent memories stored in Mem0. It acts as a bridge between AI models and the Mem0 memory system, enabling assistants to:

- Store and retrieve memories
- Search memories with semantic similarity
- Manage different memory types (episodic, semantic, procedural)
- Utilize short-term memory for conversation context
- Apply selective memory patterns
- Create knowledge graphs from memories

## Project Structure

The project has been refactored from a monolithic design to a modular structure:

```
mem0_mcp_server/
├── core/                   # Core functionality
│   ├── client.py           # Mem0 client initialization 
│   ├── logging.py          # Logging configuration
│   └── server.py           # MCP server setup
├── operations/             # Basic memory operations
│   └── basic.py            # Add, search, get, delete, update
├── memory_types/           # Specialized memory implementations
│   ├── short_term.py       # Conversation, working, attention
│   └── specialized.py      # Episodic, semantic, procedural
└── advanced/               # Advanced features
    ├── features.py         # Categories, instructions, graph, feedback
    └── selective.py        # Pattern-based memory filtering

app.py                      # Main entry point
```

## Getting Started

### Setting up in Cursor or Claude Desktop

1. Install the package:

```bash
pip install mcp-mem0-server
```

2. Add the following configuration to your MCP configuration file:

For Cursor, add this to `~/.cursor/mcp.json`:
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

3. Restart Cursor or Claude Desktop to apply the changes.

## Memory Types

The server supports different memory types organized by duration and function:

### Short-Term Memories
- **Conversation Memory**: Recall of recent message exchanges
- **Working Memory**: Temporary information being actively used 
- **Attention Memory**: Information currently in focus

### Long-Term Memories
- **Episodic Memory**: Specific events and experiences
- **Semantic Memory**: Facts, concepts, and knowledge
- **Procedural Memory**: Skills and how-to information

## Advanced Features

- **Custom Categories**: Define and manage your own memory categories
- **Memory Instructions**: Set guidelines for how memories should be processed
- **Graph Relations**: Access knowledge graph relationships between entities
- **Selective Memory**: Filter text with include/exclude patterns before storing
- **Feedback Mechanism**: Provide feedback on memory quality

## Usage

All memories in the system use "default_user" as the default user_id.

For detailed usage examples, see the [USAGE_GUIDE.md](USAGE_GUIDE.md).

## Documentation

- [Getting Started](docs/getting-started.md)
- [API Reference](docs/api-reference.md)
- [Memory Types](docs/memory-types.md)
- [Advanced Features](docs/advanced-features.md)
- [Configuration](docs/configuration.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Mem0.ai](https://mem0.ai) for their excellent memory API
- [FastMCP](https://github.com/anthropics/fastMCP) for the MCP server implementation
- All contributors to this project 