# Author: ItzRustam (Rustam Singh Bhadouriya)
# Project: NULL Multi-Agent Ecosystem | Licensed under the MIT License

"""CoreX Agent for the NULL Multi-Agent Ecosystem.

CoreX is a dedicated Code Generation sub-agent. It generates application logic,
debugs code, and structures software. It has web access via a single `web_search`
tool to look up documentation, examples, and references while coding.

This agent provides multi-agent capabilities and integrates
with web search for context-aware code generation.
"""

from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from null import corex_parser, SafeParser, corex_system_prompt  # parser
from dotenv import load_dotenv

load_dotenv()

import os
from rich import print
from null.corex.tools import web_search
from langchain_google_genai.chat_models import GoogleRateLimitError

MODEL_NAME = str(os.getenv("ALEX_MODEL"))
MAX_TOOL_CALL = int(os.getenv("MAX_TOOL_CALLS", 12))

tools_name = {
    "web_search": web_search
}

def create_corex():
    """Create the CoreX code generation agent bound to web search tool.

    CoreX generates application logic, debugs code, and structures software.
    Has web access for documentation and reference lookups.
    """
    tools = [web_search]

    # initializing 
    llm = ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=0.0, max_tokens=25000)

    agent = llm.bind_tools(tools=tools)

    return agent

def format_response(result : AIMessage):
    try:
        response = corex_parser.invoke(result)
        return response
    except Exception as E:
        response = SafeParser().parse_corex(response=result.content)
        return response

def run_corex(query : str) -> AIMessage:
    """Run CoreX
    Function to invoke CoreX for response on given `query`
    """
    # Message History will only last for given query to save memory
    message = [corex_system_prompt] # Always be reinitialized on each query as input
    
    message.append(HumanMessage(content=query))

    corex_agent = create_corex()

    # ReAct Work
    try:
        result = corex_agent.invoke(message)
        message.append(result)
    
        tool_calls = 0
        while result.tool_calls:
            if tool_calls > MAX_TOOL_CALL:
                return SafeParser.parse_corex(response="Error: Too Many Tool Called try to change MAX_TOOL_CALLS on .env")

            tool_info = result.tool_calls[0]
            chosen_tool = tools_name[tool_info["name"]]

            tool_result = chosen_tool.invoke(tool_info["args"])


            tool_result = ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_info["id"]
            )

            message.append(tool_result)

            result = corex_agent.invoke(message)
            message.append(result) # tool security
            tool_calls += 1

        return format_response(result=result)

    except GoogleRateLimitError as GRLE:
        return f"Error: {str(GRLE)} wait some time for reset this limit."
    except Exception as E:
        return f"Error: '{str(E)}'"

    
