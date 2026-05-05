#!/usr/bin/env python3
"""
Entry point for running the XML MCP server.
This script ensures proper initialization and error handling.
"""
import sys
import os

# Add src to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import asyncio
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point."""
    logger.info("Starting XML MCP Server...")
    try:
        from xml_mcp_server import main as server_main
        asyncio.run(server_main())
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
