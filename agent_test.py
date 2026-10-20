# Author: ItzRustam (Rustam Singh Bhadouriya)
# Project: NULL Multi-Agent Ecosystem | Licensed under the MIT License

"""File to test NULL for multi agent Task."""

from null.null import run_null
from rich import print

"""
In This Prompt
it should call Techno with request URL and DATA
and then Techno should call tool named `call_api`
and when NULL will receive response from Techno It will call cod
to save it in a file name result.txt
then NULL will generate summary of his work.

"""

response = run_null(query="""send a http request to url's /v1/gemini/chat with DATA = {"query" : "What is GitHub? Explain in 3 Lines", 
        "master_key": "RSRoute_my_key", 
        "model": "gemini-3.1-flash-lite",
        "temperature" : 0.7,
        "max_tokens": 2048, 
        "top_p": 1.0, 
        "end_point" : None,
        "thinking_level": None,
        "thinking_budget": None
        } and remove all values which contains None and save all api response to result.txt and show me this result also.""")
print(response)

# Test NULL, Alex and Cod connectivity
# NULL should route to Alex for research, then to Cod to create a file
response = run_null(query="Search Wikipedia for 'Python programming language' and save the summary to python_summary.txt")
print(response)


response = run_null(query="write code for a HTTP request in Go and save all the code in req.go")
print(response)