# Mem0 MCP Server 🧠

An implementation of the [Model Context Protocol](https://github.com/anthropics/model-context-protocol) for [Mem0.ai](https://mem0.ai) persistent memory.

## Overview

This MCP server provides a bridge between AI assistants (Claude, ChatGPT, etc.) and Mem0.ai's persistent memory system. It allows AI assistants to:

1. Store important information persistently across sessions
2. Retrieve relevant memories based on context
3. Build a knowledge graph of connected information
4. Organize memories into cognitive-inspired structures

## Features

- **Basic Memory Operations**: Add, search, retrieve, update, and delete memories
- **Specialized Memory Types**:
  - Short-term (conversation, working, attention context)
  - Long-term (episodic, semantic, procedural)
- **Advanced Features**:
  - Custom memory categories
  - Selective memory with includes/excludes controls
  - Custom memory processing instructions
  - Knowledge graph relationship retrieval
  - Memory quality feedback mechanism

## Installation

### Prerequisites

- Python 3.9+
- Mem0.ai API key
- [Optional] Neo4j database for graph capabilities

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/mcp-mem0-general.git
   cd mcp-mem0-general
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a configuration file:
   ```bash
   cp mcp-config.sample.json mcp-config.json
   ```

4. Add your Mem0.ai API key to the configuration file or set it as an environment variable:
   ```bash
   export MEM0_API_KEY="your-mem0-api-key"
   ```

## Usage

### Starting the Server

```bash
python main.py
```

This will start the MCP server on http://localhost:8000 by default.

### Connecting to the Server

In a Claude, ChatGPT, or other MCP-compatible client, add the server URL:
```
http://localhost:8000
```

The server provides the following tools that will be available to the AI:

```
mem0_add_memory
mem0_search_memory
mem0_get_all_memories
mem0_get_memory_by_id
mem0_delete_memory
mem0_update_memory
...and many more
```

See the [documentation](./docs/README.md) for details on all available tools.

## Documentation

Comprehensive documentation is available in the [docs directory](./docs/):

- [Getting Started Guide](./docs/getting-started.md)
- [Complete API Reference](./docs/api-reference.md) 
- [Memory Types Guide](./docs/memory-types.md)
- [Advanced Features](./docs/advanced-features.md)
- [Tutorial Collection](./docs/tutorials/)

### Loading Documentation into Memory

For a better experience, you can load the documentation directly into your Mem0 instance:

```bash
python scripts/load_docs.py
```

Once loaded, you can simply ask the AI assistant to:

```
Retrieve memory ID 76100ac4-896e-488b-90ad-036c0dfaaa80 using mem0_get_memory_by_id. 
Display only the content of the memory found, then wait for further instructions.
```

This will load the complete Mem0 usage guide directly in your chat. You can also search for specific tutorials.

## Advanced Configuration

See [Configuration Guide](./docs/configuration.md) for details on:
- Custom memory categories
- Memory extraction instructions
- Graph database integration
- Security settings

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Mem0.ai](https://mem0.ai) for their excellent memory API
- [FastMCP](https://github.com/anthropics/fastMCP) for the MCP server implementation
- All contributors to this project 