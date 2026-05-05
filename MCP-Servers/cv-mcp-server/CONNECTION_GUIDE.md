# CV MCP Server - Connection Guide

This guide explains how to connect the CV MCP Server to various MCP clients.

## Claude Desktop Configuration

Add the following to your Claude Desktop configuration file:

### Windows
Location: `%APPDATA%\Claude\claude_desktop_config.json`

### macOS
Location: `~/Library/Application Support/Claude/claude_desktop_config.json`

### Configuration

```json
{
  "mcpServers": {
    "cv-server": {
      "command": "python",
      "args": [
        "D:\\Projects\\Multi-Agent-Systems\\MCP-Servers\\cv-mcp-server\\run_server.py"
      ],
      "env": {
        "DEVICE": "cuda",
        "HF_HOME": "D:\\path\\to\\model\\cache"
      }
    }
  }
}
```

## Using with Virtual Environment

If using a virtual environment:

```json
{
  "mcpServers": {
    "cv-server": {
      "command": "D:\\Projects\\Multi-Agent-Systems\\MCP-Servers\\.venv\\Scripts\\python.exe",
      "args": [
        "D:\\Projects\\Multi-Agent-Systems\\MCP-Servers\\cv-mcp-server\\run_server.py"
      ],
      "env": {
        "DEVICE": "cuda"
      }
    }
  }
}
```

## Testing the Connection

1. **Start Claude Desktop** with the configuration above
2. **Ask Claude** to use one of the CV tools:
   - "Detect objects in this image: /path/to/image.jpg"
   - "Generate a caption for /path/to/photo.jpg"
   - "Classify this image: /path/to/picture.jpg"

## Environment Variables

- `DEVICE`: Device to use (cpu, cuda, mps)
- `HF_HOME`: Cache directory for Hugging Face models
- `HF_TOKEN`: Hugging Face token for private models

## Troubleshooting

### Server doesn't start
- Check Python path is correct
- Ensure all dependencies are installed
- Check logs in Claude Desktop developer console

### Models not downloading
- Check internet connection
- Verify HF_HOME has write permissions
- Set HF_TOKEN if accessing private models

### Slow performance
- Use GPU by setting `DEVICE=cuda`
- Use smaller model variants
- Pre-download models before first use
