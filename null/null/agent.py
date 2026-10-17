# Author: ItzRustam (Rustam Singh Bhadouriya)
# Project: NULL Multi-Agent Ecosystem | Licensed under the MIT License

"""NULL HEAD Agent ReAct Loop"""

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI # gemini model
from dotenv import load_dotenv
from rich import print
from null.null.tools import call_cod, call_techno
from warnings import filterwarnings

filterwarnings("ignore")

load_dotenv()

from langchain_google_genai import HarmCategory, HarmBlockThreshold
# For security

import os
from null import SafeParser, null_parser, null_system_prompt

MODEL_NAME = os.getenv("NULL_MODEL")
MAX_TOOL_CALL = int(os.getenv("MAX_TOOL_CALLS", 15))

# more agents will be added
agent_names = {
    "call_cod":call_cod,
    "call_techno":call_techno,
}

"""NOTE: NULL memory will be stored until the Agent runs."""

message = [null_system_prompt]

def create_null():
    agents = [call_cod, call_techno]

    llm = ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=0.2)


    agent = llm.bind_tools(tools=agents)

    return agent

def inject_success_reminder(tool_result: dict) -> str:
    """
    Generate a system reminder to prevent the LLM from repeating a successful tool call.
    """
    if tool_result.get("status") == "Success" or "Success" in str(tool_result.get("summary", "")):
        return (
            "The previous tool call completed successfully. "
            "Do NOT call the same tool with the same arguments again. "
            "Proceed to generate your final response to the user."
        )
    return ""

def run_null(query : str) -> AIMessage:
    """Do Task for Given Query
    Memory is stored and will be wiped out when agent shutdown or restarted
    """
    Null = create_null()

    message.append(HumanMessage(content=query))

    # generating first response
    try:
        result = Null.invoke(message)
        message.append(result)


        tool_calls = 0
        while result.tool_calls:
            if tool_calls > MAX_TOOL_CALL:
                return SafeParser.parse_cod(response="Error: Too Many Tool Called try to change MAX_TOOL_CALLS on .env")

            print(result)

            tool_info = result.tool_calls[0]

            chosen_tool = agent_names[tool_info["name"]]

            print(f"Null Want's to Call {tool_info}")
            approve = input("y/n: ")
            if approve.lower() == "y":
                pass
            else:
                print("User Denied The Agent Request")
                break

            tool_result = chosen_tool.invoke(tool_info["args"])

            print(f"NULL: Agent Result {tool_result}")

            tool_result = ToolMessage(
                content=tool_result,
                tool_call_id=tool_info["id"]
            )

            message.append(tool_result)
            message.append(inject_success_reminder(tool_result=tool_result.model_dump()))

            result = Null.invoke(message)
            tool_calls += 1

        print(f"LOG: NULL Called {tool_calls} Tools.")
        try:
            response = null_parser.invoke(result)
            return response
        except Exception as E:
            response = SafeParser().parse_null(response=result.content)
            return response


    except Exception as E:
        return f"Error: '{str(E)}'"


