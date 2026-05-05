#!/usr/bin/env python3
"""
Test script to verify XML MCP Server connection.
This script tests the server by simulating MCP client communication.
"""
import sys
import os
import asyncio
import subprocess
import json

async def test_server():
    """Test the server connection."""
    print("Starting XML MCP Server test...")
    
    # Start the server as a subprocess
    server_path = os.path.join(os.path.dirname(__file__), 'src', 'xml_mcp_server.py')
    
    try:
        print(f"Launching server: {server_path}")
        process = subprocess.Popen(
            [sys.executable, server_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # Send an initialize request (MCP protocol)
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-01-15",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        request_json = json.dumps(init_request) + '\n'
        print(f"Sending initialize request...")
        process.stdin.write(request_json)
        process.stdin.flush()
        
        # Read response
        print("Waiting for response...")
        response_line = process.stdout.readline()
        
        if response_line:
            response = json.loads(response_line)
            print(f"[SUCCESS] Server responded!")
            print(f"Response: {json.dumps(response, indent=2)}")
            return True
        else:
            print("[WARNING] No response from server")
            stderr = process.stderr.read()
            if stderr:
                print(f"Server stderr: {stderr}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if process:
            process.terminate()
            process.wait(timeout=5)

if __name__ == "__main__":
    result = asyncio.run(test_server())
    sys.exit(0 if result else 1)
