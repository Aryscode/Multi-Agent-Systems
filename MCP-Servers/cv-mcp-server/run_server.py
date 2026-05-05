"""
Utility script to run the CV MCP server.

This script starts the server and handles proper initialization.
"""

import asyncio
import sys
import logging

# Add the current directory to the path
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cv_mcp_server import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)
