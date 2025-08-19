#!/usr/bin/env python3
"""
Simple MCP-style Tool Server
Since the official MCP package requires Python 3.10+, this is a simple alternative
that demonstrates similar functionality.
"""

import json
import sys
from typing import Dict, Any, List
from flask import Flask, request, jsonify

app = Flask(__name__)

def count_total_rs(text: str) -> int:
    """Count the total number of 'r' characters in the given text"""
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    return text.lower().count("r")

def count_total_characters(text: str) -> int:
    """Count the total number of characters in the given text"""
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    return len(text)

def count_words(text: str) -> int:
    """Count the total number of words in the given text"""
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    return len(text.split())

# Available tools
TOOLS = {
    "count_total_rs": {
        "function": count_total_rs,
        "description": "Count the total number of 'r' characters in the given text",
        "parameters": {"text": "string - The text to analyze"}
    },
    "count_total_characters": {
        "function": count_total_characters,
        "description": "Count the total number of characters in the given text",
        "parameters": {"text": "string - The text to analyze"}
    },
    "count_words": {
        "function": count_words,
        "description": "Count the total number of words in the given text",
        "parameters": {"text": "string - The text to analyze"}
    }
}

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "server": "Simple MCP-style Tool Server",
        "available_tools": list(TOOLS.keys())
    })

@app.route('/tools', methods=['GET'])
def list_tools():
    """List all available tools"""
    tool_descriptions = {}
    for name, info in TOOLS.items():
        tool_descriptions[name] = {
            "description": info["description"],
            "parameters": info["parameters"]
        }
    return jsonify({"tools": tool_descriptions})

@app.route('/call_tool', methods=['POST'])
def call_tool():
    """Call a specific tool with provided arguments"""
    try:
        data = request.get_json()
        tool_name = data.get('tool_name')
        arguments = data.get('arguments', {})
        
        if tool_name not in TOOLS:
            return jsonify({
                "error": f"Tool '{tool_name}' not found",
                "available_tools": list(TOOLS.keys())
            }), 400
        
        # Call the tool function
        result = TOOLS[tool_name]["function"](**arguments)
        
        return jsonify({
            "tool": tool_name,
            "arguments": arguments,
            "result": result,
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 400

def run_cli():
    """Run in CLI mode for direct testing"""
    print("🔧 Simple MCP-style Tool Server - CLI Mode")
    print("Available tools:")
    for name, info in TOOLS.items():
        print(f"  - {name}: {info['description']}")
    
    while True:
        try:
            print("\nEnter tool name (or 'quit' to exit):")
            tool_name = input("> ").strip()
            
            if tool_name.lower() in ['quit', 'exit', 'q']:
                break
                
            if tool_name not in TOOLS:
                print(f"❌ Tool '{tool_name}' not found")
                continue
                
            print("Enter text to analyze:")
            text = input("> ")
            
            result = TOOLS[tool_name]["function"](text)
            print(f"Result: {result}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n Goodbye!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        run_cli()
    else:
        print("Starting Simple MCP-style Tool Server...")
        print("Server will be available at: http://127.0.0.1:5000")
        print("Available endpoints:")
        print("   GET  / - Health check and tool list")
        print("   GET  /tools - List all tools")
        print("   POST /call_tool - Call a tool")
        print("\n Run with --cli for command line mode")
        print("\n⚡ Starting server...")
        app.run(host='127.0.0.1', port=5000, debug=True)


