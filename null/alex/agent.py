# Author: ItzRustam (Rustam Singh Bhadouriya)
# Project: NULL Multi-Agent Ecosystem | Licensed under the MIT License

"""Alex Agent for the NULL Multi-Agent Ecosystem.

Alex is a dedicated Researcher sub-agent. It searches the web, Wikipedia, and ArXiv for accurate, up-to-date context and returns structured findings. It does not write code, manage files, execute APIs, or run Python scripts. Nothing much beyond research.

This agent provides multi-agent capabilities and integrates
with various tools for web search, arXiv queries, and Wikipedia lookups.
"""

from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from null import alex_parser, alex_system_prompt, SafeParser  # system prompt and parser
from dotenv import load_dotenv

load_dotenv()

import os
from rich import print
from null.alex.tools import (
    search_wikipedia,
    search_arxiv,
    web_search
) 
from langchain_google_genai.chat_models import GoogleRateLimitError

MODEL_NAME = str(os.getenv("ALEX_MODEL"))
MAX_TOOL_CALL = int(os.getenv("MAX_TOOL_CALLS", 12))

tools_name = {
    "web_search" :web_search,
    "search_wikipedia": search_wikipedia,
    "search_arxiv": search_arxiv
}

def create_alex():
    """Create the Alex researcher agent bound to web, Wikipedia, and arXiv search tools.

    Alex gathers deep context via Web, Wikipedia, and ArXiv. Nothing much beyond research.
    """
    tools = [web_search, search_wikipedia, search_arxiv]

    # initializing 
    llm = ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=0.0, max_tokens=25000)

    agent = llm.bind_tools(tools=tools)

    return agent

def format_response(result : AIMessage):
    try:
        response = alex_parser.invoke(result)
        return response
    except Exception as E:
        response = SafeParser().parse_alex(response=result.content)
        return response

def run_alex(query : str) -> AIMessage:
    """Run Alex
    Function to invoke Alex for response on given `query`
    """
    # Message History will only last for given query to save memory
    message = [] # Always be reinitialized on each query as input
    
    message.append(alex_system_prompt)
    message.append(HumanMessage(content=query))

    alex_agent = create_alex()

    # ReAct Work
    try:
        result = alex_agent.invoke(message)
        message.append(result)
    
        tool_calls = 0
        while result.tool_calls:
            if tool_calls > MAX_TOOL_CALL:
                return SafeParser.parse_alex(response="Error: Too Many Tool Called try to change MAX_TOOL_CALLS on .env")

            tool_info = result.tool_calls[0]
            chosen_tool = tools_name[tool_info["name"]]

            tool_result = chosen_tool.invoke(tool_info["args"])


            tool_result = ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_info["id"]
            )

            message.append(tool_result)

            result = alex_agent.invoke(message)
            message.append(result) # mendentory for multi-tools
            tool_calls += 1

        return format_response(result=result)

    except GoogleRateLimitError as GRLE:
        return f"Error: {str(GRLE)} wait some time for reset this limit."
    except Exception as E:
        return f"Error: '{str(E)}'"

    
