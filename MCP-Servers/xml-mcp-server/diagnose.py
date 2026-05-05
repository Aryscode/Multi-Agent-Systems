#!/usr/bin/env python3
"""
Diagnostic script to check XML MCP Server setup and configuration.
"""
import sys
import os
import subprocess
import json

def check_python():
    """Check Python version and path."""
    print("\n=== Python Configuration ===")
    print(f"Python: {sys.version}")
    print(f"Executable: {sys.executable}")
    print(f"Path: {sys.path[:3]}")
    return True

def check_imports():
    """Check if all required packages are installed."""
    print("\n=== Package Dependencies ===")
    packages = {
        'mcp': 'Model Context Protocol',
        'lxml': 'XML Library',
        'xmlschema': 'XML Schema Validation',
    }
    
    all_ok = True
    for pkg, desc in packages.items():
        try:
            __import__(pkg)
            print(f"[OK] {pkg:15} - {desc}")
        except ImportError:
            print(f"[FAIL] {pkg:15} - {desc} (NOT INSTALLED)")
            all_ok = False
    
    return all_ok

def check_files():
    """Check if all required files exist."""
    print("\n=== File Structure ===")
    base = os.path.dirname(__file__)
    files = {
        'src/xml_mcp_server.py': 'Main server',
        'src/xml_tools.py': 'XML tools',
        'pyproject.toml': 'Project config',
        'README.md': 'Documentation',
    }
    
    all_ok = True
    for file, desc in files.items():
        path = os.path.join(base, file)
        exists = os.path.exists(path)
        status = "[OK]" if exists else "[FAIL]"
        print(f"{status} {file:30} - {desc}")
        all_ok = all_ok and exists
    
    return all_ok

def check_import_server():
    """Try to import the server module."""
    print("\n=== Server Import ===")
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        from xml_mcp_server import server, TOOLS, main
        print(f"[OK] Server imported successfully")
        print(f"[OK] Found {len(TOOLS)} tools")
        print(f"[OK] Main function available")
        return True
    except Exception as e:
        print(f"[FAIL] Failed to import server: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_handlers():
    """Test handler functions."""
    print("\n=== Handler Tests ===")
    try:
        import asyncio
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        from xml_mcp_server import server, list_tools, call_tool
        from mcp.shared.exceptions import McpError
        
        async def test():
            # Test list_tools
            result = await list_tools()
            print(f"[OK] list_tools() returned {len(result)} tools")
            
            # Test invalid tool
            try:
                await call_tool("invalid_tool", {})
            except McpError:
                print(f"[OK] call_tool() properly rejects invalid tools")
            
            return True
        
        return asyncio.run(test())
    except Exception as e:
        print(f"[FAIL] Handler test failed: {e}")
        return False

def main_diagnostic():
    """Run all diagnostics."""
    print("=" * 60)
    print("XML MCP Server Diagnostic Tool")
    print("=" * 60)
    
    results = {
        'Python': check_python(),
        'Imports': check_imports(),
        'Files': check_files(),
        'Server Import': check_import_server(),
        'Handlers': check_handlers(),
    }
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    all_pass = True
    for check, result in results.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {check}")
        all_pass = all_pass and result
    
    print("=" * 60)
    
    if all_pass:
        print("\nAll checks passed!")
        print("\nServer is ready to connect:")
        print("  python src/xml_mcp_server.py")
        print("\nOr configure in Claude Desktop:")
        print('  "xml-mcp-server": {')
        print('    "command": "python",')
        print('    "args": ["path/to/xml-mcp-server/src/xml_mcp_server.py"]')
        print('  }')
        return 0
    else:
        print("\nSome checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main_diagnostic())
