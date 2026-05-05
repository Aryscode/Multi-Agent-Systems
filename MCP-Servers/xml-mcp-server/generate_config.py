#!/usr/bin/env python3
"""
Generate Claude Desktop configuration for XML MCP Server.
"""
import os
import sys
import json
from pathlib import Path

def generate_config():
    """Generate the configuration needed for Claude Desktop."""
    
    # Get the absolute path of this directory
    server_dir = os.path.dirname(os.path.abspath(__file__))
    server_script = os.path.join(server_dir, "src", "xml_mcp_server.py")
    
    config = {
        "mcpServers": {
            "xml-mcp-server": {
                "command": "python",
                "args": [server_script]
            }
        }
    }
    
    print("=" * 70)
    print("Claude Desktop Configuration Generator")
    print("=" * 70)
    
    print("\n1. Add this to your Claude Desktop config:")
    print("-" * 70)
    print(json.dumps(config, indent=2))
    print("-" * 70)
    
    print("\n2. Configuration file locations:")
    if sys.platform == "win32":
        config_path = os.path.expandvars("%APPDATA%\\Claude\\claude_desktop_config.json")
    elif sys.platform == "darwin":
        config_path = os.path.expandvars("~/Library/Application Support/Claude/claude_desktop_config.json")
    else:  # Linux
        config_path = os.path.expandvars("~/.config/Claude/claude_desktop_config.json")
    
    print(f"   Windows: %APPDATA%\\Claude\\claude_desktop_config.json")
    print(f"   macOS:   ~/Library/Application Support/Claude/claude_desktop_config.json")
    print(f"   Linux:   ~/.config/Claude/claude_desktop_config.json")
    
    print("\n3. Server path (absolute):")
    print(f"   {server_script}")
    
    print("\n4. After updating config:")
    print("   a) Restart Claude Desktop")
    print("   b) Look for 'xml-mcp-server' in available tools")
    print("   c) Try using an XML tool")
    
    print("\n5. Verify server is working:")
    print(f"   python {os.path.join(server_dir, 'diagnose.py')}")
    
    print("\n" + "=" * 70)
    print("Configuration generated successfully!")
    print("=" * 70)

if __name__ == "__main__":
    generate_config()
