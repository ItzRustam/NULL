# Author: ItzRustam (Rustam Singh Bhadouriya)
# Project: NULL Multi-Agent Ecosystem | Licensed under the MIT License

from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from null import cod_parser, cod_system_prompt, SafeParser # system prompt and parser

# Rate limit errors
from groq import RateLimitError as GroqRateLimitError
from langchain_google_genai.chat_models import GoogleRateLimitError

from dotenv import load_dotenv
load_dotenv()


COD_MODELS = ["openai/gpt-oss-120b", "gemma-4-31b-it"] # MultiModel
COD_MODELS_MAP = {
    "easy": ChatGoogleGenerativeAI(model=COD_MODELS[1], temperature=0.2,thinking_level="minimal", max_tokens=4000),
    "hard": ChatGroq(model=COD_MODELS[0], temperature=0.0, max_tokens=1500)
}


import os
from rich import print
from null.cod.tools import * # Importing Tools

MAX_TOOL_CALL = int(os.getenv("MAX_TOOL_CALLS", 15))

tools_name = {
    "create_file" : create_file,
    "create_folder" : create_folder,
    "read_file":read_file,
    "run_python_code":run_python_code,
    "get_text_length":get_text_length,
    "find_file":find_file,
}




def create_cod(difficulty : str ="easy"):
    """
    create cod a agent by binding with tools according difficulty
    """
    tools = [create_file, create_folder, read_file, run_python_code, get_text_length, find_file]
    # Multi-Model work
 
    # Hard -> 120B Groq
    # Easy -> 31B Google

    # Deciding model
    llm = COD_MODELS_MAP.get(difficulty.lower())

    agent = llm.bind_tools(tools=tools)

    return agent

def run_cod_switch(query : str, swapped_difficulty : str) -> AIMessage:
    """Run Cod By switching model when RATE LIMIT Happens
    """
    message = [] # Always be reinitialized on each query as input

    message.append(cod_system_prompt)
    message.append(HumanMessage(content=query))

    cod_agent = create_cod(difficulty=swapped_difficulty) # swapped_difficulty will be given from except of errors

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

    except GoogleRateLimitError as GRLE:
        return SafeParser.parse_cod("Rate Limit Happened even after switching the Model.") # message for NULL
    except GroqRateLimitError as GRLE:
        return SafeParser.parse_cod("Rate Limit Happened even after switching the Model.")
    except Exception as E: # Any Else Error.
        return f"Error: '{str(E)}'"

def format_response(result : AIMessage):
    try:
        response = cod_parser.invoke(result)
        return response
    except Exception as E:
        response = SafeParser().parse_cod(response=result.content)
        return response

# specialized for Called by NULL
def run_cod(query : str, difficulty : str = "easy") -> AIMessage:
    """Run Cod
    Function to invoke cod for response on given `query` and decide model on difficulty
    """
    # Message History will only last for given query to save memory
    message = [] # Always be reinitialized on each query as input

    message.append(cod_system_prompt)
    message.append(HumanMessage(content=query))

    cod_agent = create_cod(difficulty=difficulty)

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
            message.append(result)
            tool_calls += 1

        print(f"LOG: Cod Called {tool_calls} Tools.")
        return format_response(result=result)

    except GoogleRateLimitError as GRLE:
        print("COD: Google Rate Limit Hit Changing Model")
        return run_cod_switch(query=query, swapped_difficulty="hard") # Switch to Groq 120B oss-gpt Hard
    except GroqRateLimitError as GRLE:
        print("COD: Groq Rate Limit Hit Changing Model")
        return run_cod_switch(query=query, swapped_difficulty="easy") # Switch to Gemma 4 31B Google Easy
    except Exception as E:
        return f"Error: '{str(E)}'"
