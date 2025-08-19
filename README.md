# Simple-MCP-style-Tool-Server

Core Features Implemented

A small tool registry (TOOLS) that keeps track of available functions.

Three simple tools:

count_total_rs → count the number of "r"s in text

count_total_characters → count characters in text

count_words → count words in text

Flask API Endpoints:

/ → health check + available tools

/tools → list all tools with descriptions

/call_tool (POST) → call a tool with arguments

CLI mode (--cli flag) → interactively call tools from the terminal.

Inspired From

Inspired by the Model Context Protocol (MCP), but simplified.

Shows how a “tool server” concept works: define tools, expose them, let a client call them.

Makes it easy to experiment with JSON-based tool calls.
