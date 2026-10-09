# Author: ItzRustam (Rustam Singh Bhadouriya)
# Project: NULL Multi-Agent Ecosystem | Licensed under the MIT License

"""All The Agent will be wrapped as Tools"""
from langchain_core.tools import tool
from null.parsers import CodOutput
from null.cod import run_cod


# Adding Cod
@tool
def call_cod(task : str) -> CodOutput:
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

    Returns:
        CodOutput: A structured observation containing the status, task executed, and summary. If a parser conflict occurs (Fallback status or Idle task), NULL must immediately recall this tool with a simpler, broken-down task.
    """

    result : CodOutput = run_cod(query=task)
    return result

# More sub-agents will be added here soon