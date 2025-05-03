# Configuration Guide

This guide explains how to configure the Mem0 MCP Server for optimal performance and functionality.

## Configuration File

The server uses a JSON configuration file (`mcp-config.json`) for its settings. A sample file is provided (`mcp-config.sample.json`) that you can copy and modify.

```bash
cp mcp-config.sample.json mcp-config.json
```

### Basic Configuration Structure

```json
{
  "server": {
    "name": "Mem0 General Memory Server 🧠",
    "logging": {
      "level": "INFO",
      "file_path": "~/.mcp_mem0_server.log"
    }
  },
  "mem0": {
    "api_key": "YOUR_MEM0_API_KEY_HERE",
    "default_app_id": "mcp-client",
    "graph": {
      "enabled": false,
      "uri": "bolt://localhost:7687",
      "user": "neo4j",
      "password": "your_password"
    }
  }
}
```

## Server Configuration

### Server Name

The `name` field in the server section sets the display name for your MCP server. This is what users will see in their MCP-compatible clients.

```json
"name": "My Custom Memory Server"
```

### Logging Configuration

The `logging` section controls how the server logs its activity.

```json
"logging": {
  "level": "INFO",
  "file_path": "~/.mcp_mem0_server.log"
}
```

Available log levels:
- `DEBUG`: Detailed information for debugging purposes
- `INFO`: General information about server operation (default)
- `WARNING`: Information about potential issues
- `ERROR`: Information about errors that occurred
- `CRITICAL`: Information about critical errors

The `file_path` field specifies where log files are stored. You can use the tilde (`~`) to reference the user's home directory.

## Mem0 Configuration

### API Key

The most important configuration is your Mem0 API key, which you can obtain from your Mem0.ai account.

```json
"api_key": "YOUR_MEM0_API_KEY_HERE"
```

Alternatively, you can set the API key using an environment variable:

```bash
export MEM0_API_KEY="your-mem0-api-key"
```

The environment variable will override the value in the configuration file.

### Default App ID

The `default_app_id` setting specifies a default application identifier for memory operations. This is useful for filtering and analytics.

```json
"default_app_id": "my-custom-app"
```

## Graph Database Configuration

If you want to use the graph memory features, you'll need to configure a Neo4j database connection.

```json
"graph": {
  "enabled": true,
  "uri": "bolt://localhost:7687",
  "user": "neo4j",
  "password": "your_password"
}
```

### Graph Connection Options

- `enabled`: Set to `true` to enable graph features
- `uri`: Connection URI for your Neo4j database
- `user`: Neo4j database username
- `password`: Neo4j database password

If you're using a hosted Neo4j instance, update the URI accordingly:

```json
"uri": "bolt+s://your-instance-id.databases.neo4j.io:7687"
```

## Advanced Configuration

### Server Port

By default, the server runs on port 8000. To change this, add a `port` setting to the server section:

```json
"server": {
  "name": "Mem0 General Memory Server 🧠",
  "port": 8080,
  "logging": {
    "level": "INFO",
    "file_path": "~/.mcp_mem0_server.log"
  }
}
```

### Memory Defaults

You can configure default settings for memory operations:

```json
"mem0": {
  "api_key": "YOUR_MEM0_API_KEY_HERE",
  "default_app_id": "mcp-client",
  "defaults": {
    "enable_graph": true,
    "threshold": 0.65
  },
  "graph": {
    "enabled": true,
    "uri": "bolt://localhost:7687",
    "user": "neo4j",
    "password": "your_password"
  }
}
```

This example sets:
- `enable_graph` to `true` by default for memory operations
- `threshold` to `0.65` by default for search operations

## Environment Variables

In addition to configuration files, you can use environment variables for certain settings:

| Environment Variable | Description | Example |
|---------------------|-------------|---------|
| `MEM0_API_KEY` | Mem0 API key | `export MEM0_API_KEY="your-api-key"` |
| `MEM0_CONFIG_PATH` | Path to config file | `export MEM0_CONFIG_PATH="/path/to/custom-config.json"` |
| `MEM0_LOG_LEVEL` | Log level | `export MEM0_LOG_LEVEL="DEBUG"` |
| `MEM0_DEFAULT_APP_ID` | Default app identifier | `export MEM0_DEFAULT_APP_ID="my-app"` |

Environment variables take precedence over settings in the configuration file.

## Configuration Best Practices

1. **Keep Your API Key Secure**: Don't commit your API key to public repositories.
2. **Use Environment Variables in Production**: Set sensitive data using environment variables.
3. **Customize Log Paths**: Use appropriate log paths for your environment.
4. **Review Default Settings**: Adjust default settings based on your usage patterns.
5. **Enable Graph Features Selectively**: Only enable graph features when needed to optimize performance.

## Applying Configuration Changes

After modifying the configuration file, restart the server for changes to take effect:

```bash
# If running manually
python main.py

# If running as a service
sudo systemctl restart mcp-mem0-server
```

## Example Configurations

### Minimal Configuration

```json
{
  "server": {
    "name": "Mem0 Server"
  },
  "mem0": {
    "api_key": "YOUR_MEM0_API_KEY_HERE"
  }
}
```

### Development Configuration

```json
{
  "server": {
    "name": "Mem0 Dev Server",
    "port": 8000,
    "logging": {
      "level": "DEBUG",
      "file_path": "./logs/mcp_server.log"
    }
  },
  "mem0": {
    "api_key": "YOUR_MEM0_API_KEY_HERE",
    "default_app_id": "dev-environment",
    "graph": {
      "enabled": false
    }
  }
}
```

### Production Configuration

```json
{
  "server": {
    "name": "Mem0 Production Server",
    "port": 443,
    "logging": {
      "level": "WARNING",
      "file_path": "/var/log/mcp-mem0-server.log"
    }
  },
  "mem0": {
    "default_app_id": "production",
    "defaults": {
      "enable_graph": true,
      "threshold": 0.7
    },
    "graph": {
      "enabled": true,
      "uri": "bolt+s://your-instance-id.databases.neo4j.io:7687",
      "user": "neo4j",
      "password": "your_password"
    }
  }
}
```

In this production example, we're using environment variables for the API key instead of storing it in the config file. 