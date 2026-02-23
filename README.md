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

## Testing with a Simple LLM

In this example, we use Ollama to demonstrate a simple LLM with tool calling capabilities that talks to our example
MCP server. To get started, you will need to download and install Ollama from here:

```
https://ollama.com/download
```

You also will need to make sure you have llama3.1 model pulled so Ollama can
use the model in our example.

```
ollama pull llama3.1
```

Once this is done, you can run the following in a terminal to bring up the assistant:
```
python test_llm_prompt.py
```

This will start a connection with Ollama and a prompt to enter questions. Some example questions include:

1. What are the available crops?
2. What are the available crops less than $6?
3. What is the weather in Urbana?

When you are finished, type **quit** in the terminal to exit.
