# Author: ItzRustam (Rustam Singh Bhadouriya)
# Project: NULL Multi-Agent Ecosystem | Licensed under the MIT License

from langchain_core.tools import tool
from ddgs import DDGS
from warnings import filterwarnings
filterwarnings('ignore') # warnings by community edition

@tool
def web_search(query: str) -> str:
    """Search the web using DuckDuckGo and return relevant search results."""

    try:

        results = DDGS().text(
            query,
            max_results=5
        )

        if not results:
            return "No search results found."

        return "\n\n".join(
            f"Title: {result.get('title', '')}\n"
            f"URL: {result.get('href', '')}\n"
            f"Snippet: {result.get('body', '')}"
            for result in results
        )
    except Exception as E:
        return f"Error while searching web: {str(E)}"
