# Author: ItzRustam (Rustam Singh Bhadouriya)
# Project: NULL Multi-Agent Ecosystem | Licensed under the MIT License

from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from null import techno_parser, techno_system_prompt, SafeParser  # system prompt and parser
from dotenv import load_dotenv

load_dotenv()

import os
from rich import print
from null.techno.tools import call_api # only One.
from langchain_google_genai.chat_models import GoogleRateLimitError

MODEL_NAME = str(os.getenv("TECHNO_MODEL"))
MAX_TOOL_CALL = int(os.getenv("MAX_TOOL_CALLS", 15))

tools_name = {
    "call_api" : call_api
}

def create_techno():
    """
    create Techno agent on tools
    """
    tools = [call_api]

    # initializing 
    llm = ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=0.0, max_tokens=3036)

    agent = llm.bind_tools(tools=tools)

    return agent

def format_response(result : AIMessage):
    try:
        response = techno_parser.invoke(result)
        return response
    except Exception as E:
        response = SafeParser().parse_techno(response=result.content)
        return response

def run_techno(query : str) -> AIMessage:
    """Run Techno
    Function to invoke Techno for response on given `query`
    """
    # Message History will only last for given query to save memory
    message = [] # Always be reinitialized on each query as input
    
    message.append(techno_system_prompt)
    message.append(HumanMessage(content=query))

    techno_agent = create_techno()

    # ReAct Work
    try:
        result = techno_agent.invoke(message)
        message.append(result)

        tool_calls = 0
        while result.tool_calls:
            if tool_calls > MAX_TOOL_CALL:
                return SafeParser.parse_techno(response="Error: Too Many Tool Called try to change MAX_TOOL_CALLS on .env")

            tool_info = result.tool_calls[0]
            print("Current Tool Call: ", tool_info)

            chosen_tool = tools_name[tool_info["name"]]

            tool_result = chosen_tool.invoke(tool_info["args"])

            print(f"Techno: Tool Result {tool_result}")

            tool_result = ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_info["id"]
            )

            message.append(tool_result)

            result = techno_agent.invoke(message)
            message.append(result) # security
            tool_calls += 1

        print(f"LOG: Techno Called {tool_calls} Tools.")
        return format_response(result=result)

    except GoogleRateLimitError as GRLE:
        print("Techno: Google Rate Limit Hit Changing Model")
        return f"Error: {str(GRLE)}"
    except Exception as E:
        return f"Error: '{str(E)}'"

    