import asyncio
from fastmcp import Client

async def main():
    # Connect to running HTTP server
    async with Client("http://localhost:8000/sse") as client:

        # Discover what the server can do
        tools = await client.list_tools()
        # print(f"Available tools: {[tool.name for tool in tools]}")
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
        print(f"Result: {result}")

        # Read a resource
        print("\nFetching system status resource")
        status = await client.read_resource("status://current")
        print(f"Status: {status}")

        # Call the weather tool
        result = await client.call_tool("get_weather", {"city": "Champaign"})
        print(f"\nWeather result: {result}")

        # List available tables in the service
        result = await client.call_tool("list_tables")
        print(result)

        # Find an available crop
        #result = await client.call_tool("query_crop_by_name", {"name": "Soybeans"})
        result = await client.call_tool("query_crop_by_name", {"name": "*"})
        print(f"\nCrop result: {result}")





if __name__ == "__main__":
    asyncio.run(main())
