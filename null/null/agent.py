# Author: ItzRustam (Rustam Singh Bhadouriya)
# Project: NULL Multi-Agent Ecosystem | Licensed under the MIT License

"""NULL HEAD Agent ReAct Loop"""

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI # gemini model
from dotenv import load_dotenv
from rich import print
from null.null.tools import call_cod, call_techno, call_alex, call_corex
from warnings import filterwarnings
from random import randint

filterwarnings("ignore")

load_dotenv()

# For security

import os
from null import SafeParser, null_parser, null_system_prompt

MODEL_NAME = os.getenv("NULL_MODEL")
MAX_TOOL_CALL = int(os.getenv("MAX_TOOL_CALLS", 15))

# more agents will be added
agent_names = {
    "call_cod":call_cod,
    "call_techno":call_techno,
    "call_alex": call_alex,
    "call_corex": call_corex
}

"""NOTE: NULL memory will be stored until the Agent runs."""

message = [null_system_prompt]

def create_null():
    agents = [call_cod, call_techno, call_alex, call_corex]

    llm = ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=0)


    agent = llm.bind_tools(tools=agents)

    return agent

"""Tool Security - Deprecated"""
def inject_success_reminder(tool_result: dict) -> str:
    """
    Generate a system reminder to prevent the LLM from repeating a successful tool call.
    """
    print("called")
    if tool_result.get("status") == "Success" or "Success" in str(tool_result.get("summary", "")):
        print("called")
        return (
            "The previous tool call completed successfully. "
            "Do NOT call the same tool with the same arguments again. "
            "Proceed to generate your final response to the user."
        )
    return ""

class ToolSafety:
    def __init__(self):
        self.tool_used = {}
        self.tool_status = {}
    
    def check_used_tool(self, tool_name : str, tool_args : dict) -> bool:
        """Check if Tool is already used with Success Flag
        True :- Continue this Tool call
        False :- Deny It, already been called.
        """
        tool_data = {
            "name" : tool_name
        }

        # merging tool call into one clear dict
        tool_data |= tool_args
        print(tool_data)
        for tool_id, data in self.tool_used.items():
            if data == tool_data:
                status = self.tool_status.get(tool_id)
                if status == "Success":
                    return False
                else:
                    pass
            else:
                pass

        return True


    def _generate_id(self, end_range : int) -> int:
        """Generate a Unique ID for Tools data"""
        tool_id = str(randint(1, end_range))

        while tool_id in self.tool_status and tool_id in self.tool_used:
            tool_id = str(randint(1, end_range))

        return tool_id
    
    def update_used_tool(self, tool_info : dict, status : str) -> None:
        """update tool info with latest tool call"""
        tool_name = tool_info.get("name")
        args = tool_info.get("args")
        tool_data = {
            "name" : tool_name
        }

        # merging tool call into one clear dict
        tool_data |= args

        tool_id = self._generate_id(end_range=100000)
        self.tool_used[tool_id] = tool_data
        self.tool_status[tool_id] = status

def run_null(query : str) -> AIMessage:
    """Do Task for Given Query
    Memory is stored and will be wiped out when agent shutdown or restarted
    """
    Null = create_null()

    message.append(HumanMessage(content=query))
    # guard = ToolSafety() # to prevent calling same tool again and again
    # generating first response
    try:
        result = Null.invoke(message)
        message.append(result)

        tool_calls = 0
        while result.tool_calls:
            if tool_calls > MAX_TOOL_CALL:
                return SafeParser.parse_null(response="Error: Too Many Tool Called try to change MAX_TOOL_CALLS on .env")

            # print(result)

            tool_info = result.tool_calls[0]

            chosen_tool = agent_names[tool_info["name"]]

            print(f"Null Want's to Call {tool_info}")
            approve = input("y/n: ")
            if approve.lower() == "y":
                pass
            else:
                return "Tool Denied"

            """
            maybe Useful in Future

            tool_allow = guard.check_used_tool(tool_name=tool_info["name"], tool_args=tool_info["args"])
            if not(tool_allow):
                print("ToolSafety: Already used tool")
                print("Cancel/approve")
                UserInp = input("y (cancel) / n (approve): ")

                if "y" in UserInp.lower():
                    print("Stopping tool call")
                    message.append(SystemMessage(content=f"Tool {tool_info} already used for same work, continue for other task or generate a final response for user. DO NOT try to call same tool again for same work."))
                else:
                    pass
            """
            tool_result_raw = chosen_tool.invoke(tool_info["args"])

            print(f"NULL: Agent Result {tool_result_raw}")

            tool_result = ToolMessage(
                content=tool_result_raw,
                tool_call_id=tool_info["id"]
            )


            message.append(tool_result)
            result = Null.invoke(message)
            message.append(result)
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


