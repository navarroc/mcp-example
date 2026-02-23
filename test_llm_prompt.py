import ollama
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os

async def run_chat_prompt():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as client:
            await client.initialize()
            mcp_tools = await client.list_tools()

            # Convert tools to Ollama format
            ollama_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema,
                    },
                }
                for tool in mcp_tools.tools
            ]

            user = os.getenv('USER') or os.getenv('USERNAME') or os.getlogin()
            messages = []
            print("------------------------- MCP Chat Started (Type 'quit' to exit) ------------------------")
            while True:
                query = input(f"\n Hello {user}, what can I help you with today?: ")
                if query.lower() == 'quit': break

                messages.append({'role': 'user', 'content': query})

                # Send message to Ollama
                response = ollama.chat(
                    model='llama3.1',
                    messages=messages,
                    tools=ollama_tools
                )

                # Call tool
                if response.get('message', {}).get('tool_calls'):
                    for call in response['message']['tool_calls']:
                        tool_name = call['function']['name']
                        tool_args = call['function']['arguments']

                        print(f"[*] Calling MCP tool: {tool_name}({tool_args})")
                        # Call MCP server
                        result = await client.call_tool(tool_name, tool_args)
                        messages.append(response['message'])
                        messages.append({
                            'role': 'tool',
                            'content': str(result.content)
                        })

                    # Final response after tool execution
                    final_response = ollama.chat(model='llama3.1', messages=messages)
                    print(f"Assistant: {final_response['message']['content']}")
                    messages.append(final_response['message'])
                else:
                    print(f"Assistant: {response['message']['content']}")
                    messages.append(response['message'])

if __name__ == "__main__":
    try:
        asyncio.run(run_chat_prompt())
    except KeyboardInterrupt:
        pass