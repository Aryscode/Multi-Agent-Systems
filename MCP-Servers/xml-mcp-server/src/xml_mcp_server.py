import json
import logging
from typing import Any
import sys
import os

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import Server
import mcp.server.stdio
from mcp.server.lowlevel import NotificationOptions
from mcp.shared.exceptions import McpError

from xml_tools import (
    validate_xml_against_xsd,
    parse_xml_tree,
    query_xml_xpath,
    transform_xml_xslt,
    format_xml,
    generate_xml_schema,
    compare_xml_documents,
    extract_xml_namespaces,
)

# Configure logging before any other code
# Ensure logs go to stderr so they don't interfere with protocol on stdout
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr,
    force=True
)
logger = logging.getLogger(__name__)

# Initialize MCP Server
server = Server("xml-mcp-server")

# Define XML Tools
TOOLS = [
    types.Tool(
        name="validate_xml_against_xsd",
        description="Validate XML document against XSD schema",
        inputSchema={
            "type": "object",
            "properties": {
                "xml_file": {
                    "type": "string",
                    "description": "Path to XML file to validate"
                },
                "xsd_file": {
                    "type": "string",
                    "description": "Path to XSD schema file"
                }
            },
            "required": ["xml_file", "xsd_file"]
        }
    ),
    types.Tool(
        name="parse_xml_tree",
        description="Parse XML document and return tree structure",
        inputSchema={
            "type": "object",
            "properties": {
                "xml_file": {
                    "type": "string",
                    "description": "Path to XML file to parse"
                },
                "max_depth": {
                    "type": "integer",
                    "description": "Maximum depth to traverse (default: unlimited)"
                }
            },
            "required": ["xml_file"]
        }
    ),
    types.Tool(
        name="query_xml_xpath",
        description="Query XML document using XPath expression",
        inputSchema={
            "type": "object",
            "properties": {
                "xml_file": {
                    "type": "string",
                    "description": "Path to XML file"
                },
                "xpath": {
                    "type": "string",
                    "description": "XPath query expression"
                }
            },
            "required": ["xml_file", "xpath"]
        }
    ),
    types.Tool(
        name="transform_xml_xslt",
        description="Transform XML using XSLT stylesheet",
        inputSchema={
            "type": "object",
            "properties": {
                "xml_file": {
                    "type": "string",
                    "description": "Path to XML file"
                },
                "xslt_file": {
                    "type": "string",
                    "description": "Path to XSLT stylesheet"
                }
            },
            "required": ["xml_file", "xslt_file"]
        }
    ),
    types.Tool(
        name="format_xml",
        description="Format and prettify XML document",
        inputSchema={
            "type": "object",
            "properties": {
                "xml_file": {
                    "type": "string",
                    "description": "Path to XML file"
                },
                "indent": {
                    "type": "integer",
                    "description": "Indentation spaces (default: 2)"
                }
            },
            "required": ["xml_file"]
        }
    ),
    types.Tool(
        name="generate_xml_schema",
        description="Generate XSD schema from XML document",
        inputSchema={
            "type": "object",
            "properties": {
                "xml_file": {
                    "type": "string",
                    "description": "Path to XML file"
                },
                "output_file": {
                    "type": "string",
                    "description": "Path to save generated XSD file"
                }
            },
            "required": ["xml_file", "output_file"]
        }
    ),
    types.Tool(
        name="compare_xml_documents",
        description="Compare two XML documents structurally",
        inputSchema={
            "type": "object",
            "properties": {
                "xml_file1": {
                    "type": "string",
                    "description": "Path to first XML file"
                },
                "xml_file2": {
                    "type": "string",
                    "description": "Path to second XML file"
                }
            },
            "required": ["xml_file1", "xml_file2"]
        }
    ),
    types.Tool(
        name="extract_xml_namespaces",
        description="Extract all namespaces from XML document",
        inputSchema={
            "type": "object",
            "properties": {
                "xml_file": {
                    "type": "string",
                    "description": "Path to XML file"
                }
            },
            "required": ["xml_file"]
        }
    )
]

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available XML tools"""
    return TOOLS

@server.call_tool()
async def call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    """Handle tool calls"""
    if not arguments:
        raise McpError(
            types.ErrorData(code=types.INVALID_PARAMS, message="Missing arguments")
        )
    
    try:
        if name == "validate_xml_against_xsd":
            result = validate_xml_against_xsd(
                arguments["xml_file"],
                arguments["xsd_file"]
            )
        elif name == "parse_xml_tree":
            result = parse_xml_tree(
                arguments["xml_file"],
                arguments.get("max_depth")
            )
        elif name == "query_xml_xpath":
            result = query_xml_xpath(
                arguments["xml_file"],
                arguments["xpath"]
            )
        elif name == "transform_xml_xslt":
            result = transform_xml_xslt(
                arguments["xml_file"],
                arguments["xslt_file"]
            )
        elif name == "format_xml":
            result = format_xml(
                arguments["xml_file"],
                arguments.get("indent", 2)
            )
        elif name == "generate_xml_schema":
            result = generate_xml_schema(
                arguments["xml_file"],
                arguments["output_file"]
            )
        elif name == "compare_xml_documents":
            result = compare_xml_documents(
                arguments["xml_file1"],
                arguments["xml_file2"]
            )
        elif name == "extract_xml_namespaces":
            result = extract_xml_namespaces(arguments["xml_file"])
        else:
            raise McpError(
                types.ErrorData(code=types.INVALID_PARAMS, message=f"Unknown tool: {name}")
            )
        
        return [types.TextContent(type="text", text=json.dumps(result))]
    
    except McpError:
        raise
    except Exception as e:
        logger.error(f"Error calling tool {name}: {str(e)}")
        raise McpError(
            types.ErrorData(code=types.INTERNAL_ERROR, message=str(e))
        )

async def main():
    """Main entry point"""
    logger.info("=" * 50)
    logger.info("XML MCP Server starting...")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info("=" * 50)
    
    try:
        logger.info("Waiting for MCP client connection on stdio...")
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            logger.info("Client connected! Initializing MCP server...")
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="xml-mcp-server",
                    server_version="0.1.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
            logger.info("MCP server session ended")
    except EOFError:
        logger.info("Client disconnected (received EOF)")
        return
    except BrokenPipeError:
        logger.info("Client disconnected (broken pipe)")
        return
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
        return
    except Exception as e:
        logger.error(f"Server error: {type(e).__name__}: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    import asyncio
    
    # Ensure logs go to stderr so they don't interfere with protocol on stdout
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stderr,
        force=True
    )
    
    try:
        logger.info("Starting async event loop...")
        asyncio.run(main())
        logger.info("Server exited cleanly")
    except KeyboardInterrupt:
        logger.info("Interrupted")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {type(e).__name__}: {e}", exc_info=True)
        sys.exit(1)
