# Author: ItzRustam (Rustam Singh Bhadouriya)
# Project: NULL Multi-Agent Ecosystem | Licensed under the MIT License

"""All The Agent will be wrapped as Tools"""
from langchain_core.tools import tool
from null.parsers import CodOutput, TechnoOutput
from null.cod import run_cod
from null.techno import run_techno


# Adding Cod
@tool
def call_cod(task : str, difficulty : str) -> CodOutput:
    """
    Calls the COD sub-agent (File Manager) to perform local file system operations.

    Capabilities:
    Use this tool exclusively to create, read, update, delete, and list local files and directories, or to count total characters in a text block.

    Task Formatting Rules (CRITICAL):
    COD operates strictly as an execution worker without reasoning capabilities. The `task` string must be highly explicit, mechanical, and direct.
    - Provide the exact file path for every operation.
    - Provide the exact text or code payload to be written.
    - Do not instruct COD to analyze, summarize, or figure out logic.
    - Example of a correct task: "Create a file named 'main.py' and write exactly this code: 'print('Hello World')'"

    Args:
        task (str): The mechanical instruction detailing the specific file operation, exact path, and exact payload.
        difficulty (str): The difficulty set to the task MUST BE `easy` or `hard` nothing else and in small letters.

    Returns:
        CodOutput: A structured observation containing the status, task executed, and summary. If a parser conflict occurs (Fallback status or Idle task), NULL must immediately recall this tool with a simpler, broken-down task.
    """

    result : CodOutput = run_cod(query=task, difficulty=difficulty)
    return result

@tool
def call_techno(task : str) -> TechnoOutput:
    """
    Calls the TECHNO sub-agent (API Manager) to perform external API requests and integrations.
    Capabilities:
    Use this tool exclusively to send HTTP GET or POST requests to external API endpoints, retrieve real-time data, or interact with third-party services (e.g., REST APIs, GraphQL, Webhooks).
    Task Formatting Rules (CRITICAL):
    TECHNO operates strictly as an execution worker without reasoning capabilities. The `task` string must be highly explicit, mechanical, and direct.
    - Specify the exact HTTP method (e.g., "GET" or "POST").
    - Provide the full, absolute URL of the API endpoint.
    - Provide the exact JSON payload, query parameters, or request body to be sent.
    - Do not instruct TECHNO to analyze, parse, summarize, or extract meaning from the response.
    - Example of a correct task: "Send a POST request to 'https://api.example.com/v1/data' with this exact JSON payload: '{\"key\": \"value\"}'"
    Args:
    task (str): The mechanical instruction detailing the exact HTTP method, absolute URL, and exact request payload/parameters.
    Returns:
    TechnoOutput: A structured observation containing the status, task executed, summary, and raw API result. If a parser conflict occurs (Fallback status or Idle task), NULL must immediately recall this tool with a simpler, corrected task.
    """
    result : TechnoOutput = run_techno(query=task)
    return result

# More sub-agents will be added here soon