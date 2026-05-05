from fastmcp import FastMCP

# Create the server
mcp = FastMCP("My Demo Server")

# Define a tool - FastMCP automatically handles the JSON conversion
@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers together"""
    return a + b

# Run it
if __name__ == "__main__":
    mcp.run()
    print(mcp.get_tools())
    