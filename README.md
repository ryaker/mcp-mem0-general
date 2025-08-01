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

The project code is located within the `src/mcp_mem0_general/` directory.

## Installation Methods

### Method 1: DXT Extension (Recommended - Coming Soon)

The easiest way to install this MCP server will be using the DXT extension format once Claude Desktop supports it.

**Download**: [`mem0-mcp-server-0.1.0.dxt`](releases/mem0-mcp-server-0.1.0.dxt)

For detailed DXT installation instructions, see [CLAUDE_DESKTOP_INSTALL.md](CLAUDE_DESKTOP_INSTALL.md).

### Method 2: Direct Installation (Current)

This server can be run directly from GitHub using `uvx` without needing to clone the repository or install it locally.

### Running the Server

Ensure you have `uv` installed (`pipx install uv` or `brew install uv`).

You can test the server directly in your terminal:

```bash
# Make sure MEM0_API_KEY is set in your environment
export MEM0_API_KEY="your-mem0-api-key-here"

# Run the server using uvx
uvx git+https://github.com/ryaker/mcp-mem0-general.git mcp-mem0-general
```

The server should start and log its initialization steps.

### Method 3: Manual Configuration in Claude Desktop/Cursor

1.  **Find `uvx` Path:** GUI applications like Claude Desktop often don't use the same `PATH` as your terminal. Find the full path to your `uvx` executable by running this in your terminal:
    ```bash
    which uvx
    ```
    Copy the output path (e.g., `/Users/yourname/.local/bin/uvx` or `/opt/homebrew/bin/uvx`).

2.  **Configure MCP:** Add the following configuration to your MCP configuration file, **replacing `/full/path/to/uvx`** with the actual path you found in step 1.

    *   **Cursor:** Add/update in `~/.cursor/mcp.json`:
    *   **Claude Desktop:** Add/update a similar configuration in your settings.

    ```json
    "mem0-memory-general": {
      "command": "/full/path/to/uvx", # <-- IMPORTANT: Use the full path from 'which uvx'
      "args": [
        "git+https://github.com/ryaker/mcp-mem0-general.git",
        "mcp-mem0-general"
      ],
      "env": {
        "MEM0_API_KEY": "your-mem0-api-key-here"
      }
    }
    ```

3.  **Restart:** Restart Cursor or Claude Desktop to apply the changes. The server should now start correctly within the application.

For detailed Claude Desktop installation instructions and troubleshooting, see [CLAUDE_DESKTOP_INSTALL.md](CLAUDE_DESKTOP_INSTALL.md).

### Note on `mem0ai[neo4j]` Warning

You might see a warning like `warning: The package mem0ai==0.1.96 does not have an extra named neo4j` during startup.

*   **If using the managed Mem0.ai platform:** This warning can be safely ignored. The necessary graph processing happens server-side on the Mem0 platform.
*   **If self-hosting Mem0 with Neo4j:** This warning indicates that the specific `mem0ai` version didn't automatically install Neo4j-related Python libraries (`langchain-neo4j`, `neo4j`). You would need to ensure these are installed manually in your self-hosted environment if using graph features.

## Loading the Usage Guide into Memory (Recommended)

To make it easy for your AI assistant to reference the server's capabilities, you can load the `USAGE_GUIDE.md` content into Mem0. Follow these steps:

**Prerequisite:** Ensure the Mem0 MCP server is running and configured correctly in your AI assistant (Claude/Cursor) as described in the "Getting Started" section above.

1.  **Copy the Guide Content:** Open the [USAGE_GUIDE.md](USAGE_GUIDE.md) file. Select and copy its *entire* text content.

2.  **Ask Assistant to Add Memory:** Go to your AI assistant (Claude/Cursor) and use a prompt similar to this, pasting the guide content you copied where indicated. Make sure to use your consistent `user_id` (e.g., "default_user").

    ```
Please remember the following usage guide for the Mem0 MCP server. Use user_id "default_user" and add metadata `{"title": "Mem0 MCP Usage Guide", "source": "README Instruction"}`:

[--- PASTE THE ENTIRE USAGE_GUIDE.md CONTENT HERE ---]
```

    The assistant should call the `mem0_add_memory` tool.

3.  **Find the Memory ID:** Once the assistant confirms the memory is added, ask it to find the specific ID for that memory:

    ```
Please search my memories for user_id "default_user" using the query "Mem0 MCP Usage Guide" and tell me the exact memory ID of that guide memory you just added.
```

    The assistant should use the `mem0_search_memory` tool and provide you with an ID string (e.g., `76100ac4-896e-488b-90ad-036c0dfaaa80`). **Note down this ID!**

4.  **Retrieve the Guide Later:** Now that you have the ID, you can quickly ask your assistant to recall the full guide anytime using a prompt like this:

    ```
    First execute Retrieve memory ID *your-guide-id-here* using mem0_get_memory_by_id. Then return control to me.
    ```

    (Replace *`your-guide-id-here`* with the actual ID you noted down in step 3).

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
- [Model Context Protocol](https://modelcontextprotocol.io/) (and its Python SDK `mcp`) for the server implementation
- All contributors to this project 