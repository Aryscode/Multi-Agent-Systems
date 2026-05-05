#!/usr/bin/env python3
"""
XML MCP Server - Direct launcher with debug output.
Use this when testing or debugging server startup.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print(f"Python: {sys.version}", file=sys.stderr)
print(f"CWD: {os.getcwd()}", file=sys.stderr)
print(f"Module path: {sys.path[0]}", file=sys.stderr)

# Now import and run
if __name__ == "__main__":
    import asyncio
    from xml_mcp_server import main
    
    print("Starting server...", file=sys.stderr)
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
