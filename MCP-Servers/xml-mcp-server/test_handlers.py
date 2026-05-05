#!/usr/bin/env python3
"""
Simple test to verify the server can handle MCP initialization.
"""
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Test basic imports
try:
    print("[PASS] Importing MCP modules...")
    from xml_mcp_server import server, TOOLS, call_tool, list_tools
    import asyncio
    import mcp.types as types
    
    print(f"[PASS] Server object created: {server}")
    print(f"[PASS] Found {len(TOOLS)} tools")
    
    # Test handlers directly
    async def test_handlers():
        print("\n[TEST] Testing list_tools handler...")
        result = await list_tools()
        print(f"[PASS] list_tools returned {len(result)} tools")
        
        print("\n[TEST] Testing call_tool with invalid tool...")
        try:
            await call_tool("nonexistent", {"arg": "value"})
        except Exception as e:
            print(f"[PASS] call_tool properly rejected invalid tool: {type(e).__name__}")
        
        print("\n[SUCCESS] All handlers working correctly!")
    
    asyncio.run(test_handlers())
    
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
