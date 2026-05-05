# XML MCP Server

A comprehensive Model Context Protocol (MCP) server for XML processing with tools for validation, parsing, querying, transformation, and schema generation.

## Features

- **XML Validation**: Validate XML documents against XSD schemas
- **XML Tree Parsing**: Parse and traverse XML document structure
- **XPath Queries**: Query XML using XPath expressions
- **XSLT Transformation**: Transform XML using XSLT stylesheets
- **XML Formatting**: Prettify and format XML documents
- **Schema Generation**: Generate XSD schemas from XML documents
- **XML Comparison**: Compare two XML documents structurally
- **Namespace Extraction**: Extract and list all namespaces in XML

## Installation

```bash
cd xml-mcp-server
pip install -e .
```

## Usage

### Direct Execution

```bash
# Run the server directly
python src/xml_mcp_server.py

# Or use the wrapper script
python run_server.py
```

### Integration with MCP Client

To connect from an MCP client (e.g., Claude Desktop), configure it to run:

```json
{
  "xml-mcp-server": {
    "command": "python",
    "args": [
      "path/to/xml-mcp-server/src/xml_mcp_server.py"
    ]
  }
}
```

Or use the wrapper script:

```json
{
  "xml-mcp-server": {
    "command": "python",
    "args": [
      "path/to/xml-mcp-server/run_server.py"
    ]
  }
}
```

## Available Tools

1. `validate_xml_against_xsd` - Validate XML against XSD schema
2. `parse_xml_tree` - Parse and display XML tree structure
3. `query_xml_xpath` - Query XML using XPath expressions
4. `transform_xml_xslt` - Transform XML with XSLT
5. `format_xml` - Format and prettify XML
6. `generate_xml_schema` - Generate XSD from XML
7. `compare_xml_documents` - Compare two XML files
8. `extract_xml_namespaces` - Extract namespace information

## Dependencies

- `lxml` - XML processing library
- `xmlschema` - XSD validation and schema generation
- `mcp` - Model Context Protocol framework
