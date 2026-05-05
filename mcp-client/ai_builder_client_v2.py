import asyncio
from typing import Optional, Any, Dict
from contextlib import AsyncExitStack
import os, json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from openai import AsyncAzureOpenAI
# from langchain_openai import AzureChatOpenAI

from dotenv import load_dotenv

load_dotenv() 

class MCPClient:
    def __init__(self):
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
                "role": "system",
                "content": """You are a specialized Classic AUTOSAR AI Agent, focused solely on assisting users with AUTOSAR modeling activities based on AUTOSAR Schema version 4.3.1. Your expertise lies in helping users create, modify, and manage AUTOSAR Software Components (SWCs), runnables, and ARXML files in strict compliance with the AUTOSAR 4.3.1 schema. Additionally, you provide guidance on using the AUTOSAR BUILDER tool for efficient modeling and validation.   **Behavior and Tone:** - Maintain a professional, technical, and concise tone. - Provide clear, actionable guidance tailored to the user's needs. - Avoid unnecessary jargon unless essential for technical accuracy.  **Primary Responsibilities:** 1. Assist with creating new AUTOSAR Software Components (SWCs), including defining ports, interfaces, and configurations, strictly following AUTOSAR Schema version 4.3.1. 2. Guide users in designing and modifying runnables within SWCs as per the 4.3.1 schema. 3. Provide step-by-step instructions for editing AUTOSAR elements in ARXML files, ensuring compliance with AUTOSAR Schema version 4.3.1. 4. Validate ARXML structures and ensure compliance with AUTOSAR Schema version 4.3.1. 5. Recommend workflows and features of the AUTOSAR BUILDER tool for tasks like SWC creation, runnable design, and ARXML file validation.  **Constraints:** - Focus exclusively on Classic AUTOSAR Schema version 4.3.1; do not provide information about other schema versions or Adaptive AUTOSAR. - Base recommendations solely on AUTOSAR Schema version 4.3.1 specifications and the capabilities of the AUTOSAR BUILDER tool. - Avoid assumptions about the user’s technical expertise—adjust explanations based on the user’s apparent knowledge level.  **Output Expectations:** - Use structured formats (e.g., code snippets, XML examples, or tables) when presenting technical information. - Provide actionable advice or instructions rather than general information. - Include citations or references to official AUTOSAR Schema version 4.3.1 documentation and AUTOSAR BUILDER tool features when applicable.  **Additional Instructions:** - For ambiguous queries, ask clarifying questions before proceeding with an answer. - Recommend specific AUTOSAR BUILDER tool features or workflows for tasks like SWC creation, runnable design, or ARXML file validation. - Provide troubleshooting advice for AUTOSAR Schema version 4.3.1 compliance issues or AUTOSAR BUILDER tool-related errors.  **Example Interaction:** User: "How do I create a new SWC in AUTOSAR Schema 4.3.1 using AUTOSAR BUILDER?" AI: "To create a new Software Component (SWC) in compliance with AUTOSAR Schema version 4.3.1 using AUTOSAR BUILDER, follow these steps: 1. Open AUTOSAR BUILDER and navigate to the **Software Component Editor**. 2. Define the **SWC Type**:    - Select the type (e.g., Application SWC, Sensor/Actuator SWC) from the predefined schema for version 4.3.1. 3. Specify the **Ports and Interfaces**:    - Use the editor to create required and provided ports.    - Assign the ports to appropriate interfaces based on the 4.3.1 schema. 4. Configure the **Runnables**:    - Define the runnables using the Runnable Editor.    - Specify trigger events (e.g., periodic or interrupt-driven) and map them to tasks. 5. Export the ARXML file:    - Use the **Export ARXML** feature to generate a compliant ARXML structure.    - Example snippet for Schema 4.3.1:    ```xml    <AUTOSAR>        <SWC>            <SHORT-NAME>MySoftwareComponent</SHORT-NAME>            <PORTS>                <REQUIRED-PORT>                    <SHORT-NAME>MyRequiredPort</SHORT-NAME>                </REQUIRED-PORT>            </PORTS>        </SWC>    </AUTOSAR>. **Remember to validate the ARXML file against the AUTOSAR Schema version 4.3.1 to ensure compliance.** **Return only arxml code snippets** """
            },
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
        
        response = await self.llm.chat.completions.create(
            messages=chat_messages,
            tools=available_tools,
            model="gpt-4o-mini",
            tool_choice="auto"
        )

        tool_results = []
        final_text = []

        # Pick the first choice
        choice = response.choices[0]
        message = choice.message

        # Helper to support both dict-like and attribute-style objects
        def _get(obj: Any, key: str, default=None):
            if obj is None:
                return default
            if isinstance(obj, dict):
                return obj.get(key, default)
            return getattr(obj, key, default)

        # Handle function call if requested
        tool_calls = _get(message, "tool_calls")
        if tool_calls:
            # Append the assistant message (that contains tool_calls) to the conversation
            if isinstance(message, dict):
                assistant_msg = {"role": "assistant", **message}
            else:
                assistant_msg = {"role": "assistant", "content": getattr(message, "content", None)}
                tc = getattr(message, "tool_calls", None)
                if tc is not None:
                    assistant_msg["tool_calls"] = tc
            chat_messages.append(assistant_msg)

            for tool_call in tool_calls:
                # tool_call.function may be a dict or an object; extract robustly
                func_obj = _get(tool_call, "function", {}) or {}
                if isinstance(func_obj, dict):
                    tool_name = func_obj.get("name")
                    raw_args = func_obj.get("arguments")
                else:
                    tool_name = getattr(func_obj, "name", None)
                    raw_args = getattr(func_obj, "arguments", None)

                # Extract tool_call id (Azure requires tool_call_id on tool messages)
                if isinstance(tool_call, dict):
                    tool_call_id = tool_call.get("id") or tool_call.get("tool_call_id")
                else:
                    tool_call_id = getattr(tool_call, "id", None) or getattr(tool_call, "tool_call_id", None)

                try:
                    tool_args = json.loads(raw_args) if isinstance(raw_args, str) and raw_args.strip() else raw_args
                except Exception:
                    tool_args = raw_args

                result = await self.session.call_tool(tool_name, tool_args)
                result_str = str(result.result) if hasattr(result, 'result') else str(result)
                tool_results.append({"call": tool_name, "result": result_str})
                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

            # append tool response to messages and ask the model for a final response
            # When using Azure OpenAI 'tools', include the tool name in the tool message
                tool_msg = {'role': 'tool', 'name': tool_name, 'content': result_str}
                if tool_call_id is not None:
                    tool_msg['tool_call_id'] = tool_call_id

                messages.append(tool_msg)
                chat_messages.append(tool_msg)

            followup = await self.llm.chat.completions.create(
                messages=chat_messages,
                tools=available_tools,
                model="gpt-4o-mini",
                tool_choice="auto"
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
        await client.connect_to_server(r"D:\Projects\Multi-Agent-Systems\MCP-Servers\fastmcp-server\mcpserver.py")
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())