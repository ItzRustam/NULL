# Author: ItzRustam (Rustam Singh Bhadouriya)
# Project: NULL Multi-Agent Ecosystem | Licensed under the MIT License

"""NULL HEAD Agent ReAct Loop"""

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI # gemini model
from dotenv import load_dotenv
from rich import print
from null.null.tools import call_cod
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
    "call_cod":call_cod
}

"""NOTE: NULL memory will be stored until the Agent runs."""

message = [null_system_prompt]

def create_null():
    agents = [call_cod]

    llm = ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=0.3,
                                 safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    })


    agent = llm.bind_tools(tools=agents)

    return agent

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

            result = Null.invoke(message)
            tool_calls += 1

        print(f"LOG: NULL Called {tool_calls} Tools.")
        try:
            response = null_parser.invoke(result)
            return response
        except Exception as E:
            response = SafeParser().parse_null(response=result)
            return response


    except Exception as E:
        return f"Error: '{str(E)}'"


