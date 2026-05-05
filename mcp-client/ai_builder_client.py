import asyncio
from typing import Optional, Any, Dict
from contextlib import AsyncExitStack
import os, json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Use Azure OpenAI async client (openai package)
from openai import AsyncAzureOpenAI
# from langchain_openai import AzureChatOpenAI

from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env


class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

        self.llm = AsyncAzureOpenAI(api_version="2024-08-01-preview")

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server
        
        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")
            
        command = "uv" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=["run", server_script_path, "D:/Projects/mcp-filesystem"],
            env=None
        )
        
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        
        await self.session.initialize()
        
        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def process_query(self, query: str) -> str:
        """Process a query using Azure OpenAI and available tools"""
        messages = [
            {
                "role": "user",
                "content": query
            }
        ]

        response = await self.session.list_tools()

        # Convert MCP tools to OpenAI function-compatible format
        available_tools = [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema
            }
        } for tool in response.tools]

        # Prepare messages for OpenAI
        chat_messages = [{"role": m.get("role"), "content": m.get("content")} for m in messages]

        # Prepare functions list for OpenAI if any tools exist
        functions = []
        for t in available_tools:
            func = t.get("function", {})
            functions.append({
                "name": func.get("name"),
                "description": func.get("description"),
                "parameters": func.get("parameters") or {}
            })

        # Create chat completion (async)
        response = await self.llm.chat.completions.create(
            messages=chat_messages,
            functions=functions,
            model="gpt-4o-mini"
        )

        tool_results = []
        final_text = []

        # Pick the first choice
        choice = response.choices[0]
        message = choice.message

        # Handle function call if requested
        if getattr(message, 'function_call', None) or (isinstance(message, dict) and message.get('function_call')):
            func_call = getattr(message, 'function_call', None) or message.get('function_call')
            tool_name = func_call.get('name')
            raw_args = func_call.get('arguments')
            try:
                tool_args = json.loads(raw_args) if isinstance(raw_args, str) else raw_args
            except Exception:
                tool_args = raw_args

            result = await self.session.call_tool(tool_name, tool_args)
            result_str = str(result.result) if hasattr(result, 'result') else str(result)
            tool_results.append({"call": tool_name, "result": result_str})
            final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

            # append tool response to messages and ask the model for a final response
            messages.append({'role': 'tool', 'content': result_str, 'tool_name': tool_name})
            chat_messages.append({"role": "tool", "content": result_str})

            followup = await self.llm.chat.completions.create(
                messages=chat_messages,
                functions=functions,
                model="gpt-4o-mini"
            )
            follow_choice = followup.choices[0]
            follow_message = follow_choice.message
            if isinstance(follow_message, dict):
                final_content = follow_message.get('content')
            else:
                final_content = getattr(follow_message, 'content', None)
            final_text.append(final_content)
        else:
            # Direct content answer
            if isinstance(message, dict):
                content = message.get('content')
            else:
                content = getattr(message, 'content', None)
            final_text.append(content)
        return "\n".join(final_text)

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")
        
        while True:
            try:
                query = input("\nQuery: ").strip()
                
                if query.lower() == 'quit':
                    break
                    
                response = await self.process_query(query)
                print("\n" + response)
                    
            except Exception as e:
                print(f"\nError: {str(e)}")
    
    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()


async def main():  
    client = MCPClient()
    try:
        await client.connect_to_server(r"D:\Projects\Multi-Agent-Systems\filesystem_server.py")
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())