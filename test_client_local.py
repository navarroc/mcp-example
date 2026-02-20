import asyncio
from fastmcp import Client

async def main():

    client = Client("server.py")
    async with client:
        # Discover what the server can do
        print("What tools are available?")
        tools = await client.list_tools()
        for tool in tools:
            print(tool.name)
            print(tool.description)
            print("Expected Inputs (JSON Schema): ")
            print(tool.inputSchema)
            print("-" * 20)

        # Call the add numbers tool
        result = await client.call_tool(
            "add_numbers",
            {"val1": 6, "val2": 7}
        )
        print(f"\nAdd Number tool result: {result}")

        # Read a resource
        print("\nFetching system status resource")
        status = await client.read_resource("status://current")
        print(f"Status: {status}")

        # Call the weather tool
        result = await client.call_tool("get_weather", {"city": "Champaign"})
        print(f"\nWeather result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
