# Claude Desktop Installation Guide

This guide provides multiple ways to install the Mem0 MCP Server in Claude Desktop.

## Method 1: DXT Extension (Recommended - Coming Soon)

> **Note**: DXT extension support is coming to Claude Desktop. This will be the easiest installation method once available.

1. **Download the Extension**
   - Download `mem0-mcp-server-0.1.0.dxt` from the [releases](releases/) directory
   - Or download directly from GitHub releases (when available)

2. **Install in Claude Desktop**
   - Open Claude Desktop
   - Go to Settings → Extensions
   - Click "Install Extension"
   - Select the downloaded `.dxt` file
   - Enter your `MEM0_API_KEY` when prompted

3. **Verify Installation**
   - Restart Claude Desktop
   - The Mem0 tools should now be available in your conversations

## Method 2: Manual MCP Configuration (Current)

Since DXT support isn't yet available in Claude Desktop, use this manual method:

### Prerequisites

- Ensure you have `uv` installed: `brew install uv` or `pipx install uv`
- Get your Mem0 API key from [mem0.ai](https://mem0.ai)

### Configuration Steps

1. **Find your Claude Desktop config directory**
   ```bash
   # On macOS
   ls ~/Library/Application\ Support/Claude/
   ```

2. **Edit or create the MCP configuration file**
   
   **File location**: `~/Library/Application Support/Claude/claude_desktop_config.json`

3. **Add the Mem0 server configuration**
   ```json
   {
     "mcpServers": {
       "mem0-memory-general": {
         "command": "uvx",
         "args": [
           "git+https://github.com/ryaker/mcp-mem0-general.git",
           "mcp-mem0-general"
         ],
         "env": {
           "MEM0_API_KEY": "your-mem0-api-key-here"
         }
       }
     }
   }
   ```

4. **Important**: Replace `your-mem0-api-key-here` with your actual Mem0 API key

5. **Find the full path to uvx**
   ```bash
   which uvx
   ```
   
   If the output is something like `/opt/homebrew/bin/uvx`, update your configuration:
   ```json
   {
     "mcpServers": {
       "mem0-memory-general": {
         "command": "/opt/homebrew/bin/uvx",
         "args": [
           "git+https://github.com/ryaker/mcp-mem0-general.git", 
           "mcp-mem0-general"
         ],
         "env": {
           "MEM0_API_KEY": "your-mem0-api-key-here"
         }
       }
     }
   }
   ```

6. **Restart Claude Desktop** to apply the changes

### Verification

After restarting Claude Desktop, you should see the Mem0 tools available. Test with:

```
Please search my memories for user_id "default_user" with the query "test"
```

Claude should respond using the `mem0_search_memory` tool.

## Available Tools

Once installed, you'll have access to 18 memory tools:

### Core Memory Operations
- `mem0_add_memory` - Add memories with inference
- `mem0_add_memory_direct` - Add memories bypassing inference
- `mem0_search_memory` - Search memories with semantic similarity
- `mem0_get_all_memories` - Retrieve all memories with pagination
- `mem0_get_memory_by_id` - Get specific memory by ID
- `mem0_delete_memory` - Delete memories
- `mem0_update_memory` - Update existing memories

### Specialized Memory Types
- `mem0_add_short_term_memory` - Session-specific contextual memory
- `mem0_add_episodic_memory` - Specific events and experiences
- `mem0_add_semantic_memory` - Facts and knowledge
- `mem0_add_procedural_memory` - Skills and processes

### Advanced Features
- `mem0_update_categories` - Manage custom memory categories
- `mem0_get_categories` - View current categories
- `mem0_set_instructions` - Set memory extraction guidelines  
- `mem0_get_instructions` - View current instructions
- `mem0_get_graph_relations` - Explore knowledge graph connections
- `mem0_send_feedback` - Improve memory quality
- `mem0_add_memory_selective` - Selective memory with filters

## Troubleshooting

### Common Issues

1. **"MEM0_API_KEY not found" error**
   - Verify your API key is correct in the configuration
   - Ensure there are no extra spaces or quotes around the key

2. **"uvx command not found" error**
   - Install uv: `brew install uv` or `pipx install uv`
   - Use the full path to uvx in your configuration

3. **Server fails to start**
   - Check the Claude Desktop logs (usually in Console.app on macOS)
   - Verify your internet connection for downloading dependencies

4. **Tools not appearing**
   - Ensure you restarted Claude Desktop after configuration changes
   - Check that the JSON configuration is valid (no trailing commas, proper quotes)

### Getting Help

- Check the [USAGE_GUIDE.md](USAGE_GUIDE.md) for detailed tool usage
- Review [troubleshooting docs](docs/configuration.md)
- Open an issue on [GitHub](https://github.com/ryaker/mcp-mem0-general/issues)

## Default User ID

All memory operations use `"default_user"` as the default user_id unless specified otherwise.