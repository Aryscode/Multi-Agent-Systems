# XML MCP Server Connection Guide

## Server Status: READY

The XML MCP Server is properly configured and ready for client connections.

### Server Details
- **Name**: xml-mcp-server
- **Version**: 0.1.0
- **Transport**: stdio (standard input/output)
- **Language**: Python 3.8+

### Registered Tools (8 total)
1. `validate_xml_against_xsd` - Validate XML against XSD schema
2. `parse_xml_tree` - Parse XML and display tree structure  
3. `query_xml_xpath` - Query XML using XPath expressions
4. `transform_xml_xslt` - Transform XML using XSLT
5. `format_xml` - Format and prettify XML documents
6. `generate_xml_schema` - Generate XSD schema from XML
7. `compare_xml_documents` - Compare two XML files structurally
8. `extract_xml_namespaces` - Extract namespace information

### How to Connect

#### Option 1: Direct Execution
```bash
cd xml-mcp-server
python src/xml_mcp_server.py
```

#### Option 2: Using Wrapper Script
```bash
cd xml-mcp-server
python run_server.py
```

#### Option 3: Claude Desktop Configuration
Add to your Claude Desktop configuration file (~/.config/Claude/claude_desktop_config.json on Linux/Mac, or %APPDATA%\Claude\claude_desktop_config.json on Windows):

```json
{
  "mcpServers": {
    "xml-server": {
      "command": "python",
      "args": ["/path/to/xml-mcp-server/src/xml_mcp_server.py"]
    }
  }
}
```

Or with the wrapper:

```json
{
  "mcpServers": {
    "xml-server": {
      "command": "python",
      "args": ["/path/to/xml-mcp-server/run_server.py"]
    }
  }
}
```

### Troubleshooting Connection Issues

#### Issue: "Connection refused" or "Cannot connect to server"
**Solution**: Ensure the server path is correct and Python is in your PATH

#### Issue: "Module not found" errors
**Solution**: Install dependencies:
```bash
pip install mcp lxml xmlschema
```

#### Issue: Server starts but client gets no response
**Solution**: Check that stdio streams are properly connected. The server communicates via JSON-RPC over stdin/stdout.

### Testing the Server

To test if the server is working:

```bash
python test_connection.py
```

### Server Architecture

- **Framework**: MCP (Model Context Protocol) Python SDK
- **Protocol**: JSON-RPC 2.0 over stdio
- **Handler Pattern**: Async request handlers for listing and calling tools
- **Error Handling**: Proper MCP error codes and messages
- **Dependencies**: lxml (XML processing), xmlschema (XSD validation)

### Protocol Flow

1. Client launches server as subprocess
2. Client sends `initialize` request via stdin
3. Server responds with capabilities
4. Client can now call `list_tools` or `call_tool` requests
5. Server processes requests and returns results via stdout
6. All communication is JSON-RPC 2.0 format

### File Structure

```
xml-mcp-server/
├── src/
│   ├── xml_mcp_server.py      # Main server entry point
│   └── xml_tools.py            # XML tool implementations
├── run_server.py               # Wrapper script
├── test_connection.py          # Connection test script
├── pyproject.toml              # Project configuration
└── README.md                   # Documentation
```

### Support

For issues or questions:
1. Check the server logs (stderr output)
2. Verify all XML files are accessible
3. Ensure proper permissions on files
4. Check that stdin/stdout are connected properly in your MCP client configuration
