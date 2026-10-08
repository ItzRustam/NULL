# Author: ItzRustam (Rustam Singh Bhadouriya)
# Project: NULL Multi-Agent Ecosystem | Licensed under the MIT License

from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langchain_ollama import ChatOllama
from null import cod_parser, cod_system_prompt, SafeParser # system prompt and parser

from dotenv import load_dotenv
load_dotenv()


import os
from rich import print
from null.cod.tools import * # Importing Tools

MODEL_NAME = str(os.getenv("COD_MODEL"))
MAX_TOOL_CALL = int(os.getenv("MAX_TOOL_CALLS", 15))

tools_name = {
    "create_file" : create_file,
    "create_folder" : create_folder,
    "read_file":read_file,
    "run_python_code":run_python_code,
    "get_text_length":get_text_length,
    "find_file":find_file
}

def create_cod():
    """
    create cod a agent by binding with tools
    """
    tools = [create_file, create_folder, read_file, run_python_code, get_text_length, find_file]
    # llm any 8B model
    llm = ChatOllama(model=MODEL_NAME, temperature=0, keep_alive="0")

    agent = llm.bind_tools(tools=tools)

    return agent

# specialized for Called by NULL
def run_cod(query : str) -> AIMessage:
    """Run Cod
    Function to invoke cod for response on given `query`
    """
    # Message History will only last for given query to save memory
    message = [] # Always be reinitialized on each query as input

    message.append(cod_system_prompt)
    message.append(HumanMessage(content=query))

    cod_agent = create_cod()

    # generating first response
    try:
        result = cod_agent.invoke(message)
        message.append(result)

        tool_calls = 0
        while result.tool_calls:
            if tool_calls > MAX_TOOL_CALL:
                return SafeParser.parse_cod(response="Error: Too Many Tool Called try to change MAX_TOOL_CALLS on .env")

            tool_info = result.tool_calls[0]
            print("Current Tool Call: ", tool_info)

            chosen_tool = tools_name[tool_info["name"]]

            tool_result = chosen_tool.invoke(tool_info["args"])

            print(f"COD: Tool Result {tool_result}")

            tool_result = ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_info["id"]
            )

            message.append(tool_result)

            result = cod_agent.invoke(message)
            tool_calls += 1

        print(f"LOG: Cod Called {tool_calls} Tools.")
        try:
            response = cod_parser.invoke(result)
            return response
        except Exception as E:
            response = SafeParser().parse_cod(response=result)
            return response


    except Exception as E:
        return f"Error: '{str(E)}'"
