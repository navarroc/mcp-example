This is a simple MCP server that provides a few different examples of how tools
can be defined.

## Requirements

Install virtualenv or conda for python 3. Run:

```
pip install -r requirements.txt
```

## Running the MCP Server

By default, server.py runs using the stdio transport.

```
python server.py
```

Alternatively, you can uncomment the line mcp.run(transport="sse") in server.py
and run the above command again to use SSE transport to connect over Http.

## Testing the MCP Server

If you are running the server with http/sse, use test_client_http.py

If you are not running the server, you can just run test_client_local.py
to run the server in stdio transport mode.

## Testing with Claude Desktop

The easiest way to test this with Claude Desktop is to use the stdio transport. Find the file
claude_desktop_config.json and add a local MCP server. For example:

```
"mcpServers": {
    "aifarms": {
      "command": "/path/to/virtualenv/mcp-example/venv/bin/python3",
      "args": [
        "/path/to/source/mcp-example/server.py"
      ],
      "env": {
        "PYTHONPATH": "/path/to/source/mcp-example"
      }
    }
  }
```

Restart Claude Desktop and you should be able to run the following prompt:

```
What crops are less than $6?
```
