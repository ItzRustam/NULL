# Author: ItzRustam (Rustam Singh Bhadouriya)
# Project: NULL Multi-Agent Ecosystem | Licensed under the MIT License

from langchain_core.tools import tool
from ddgs import DDGS
import wikipedia as wk
import arxiv
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

@tool
def search_arxiv(query: str) -> str:
    """Searches arXiv for scientific research papers and returns their summaries.
    
    Use this tool to find academic publications, abstracts, and authors.
    """
    client = arxiv.Client()
    
    search = arxiv.Search(
        query=query,
        max_results=2,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    try:
        results = []
        for paper in client.results(search):
            paper_info = (
                f"Published: {paper.published.date()}\n"
                f"Title: {paper.title}\n"
                f"Authors: {', '.join(author.name for author in paper.authors)}\n"
                f"Summary: {paper.summary}\n"
                f"URL: {paper.pdf_url}\n"
                f"{'-'*40}"
            )
            results.append(paper_info)
            
        if not results:
            return f"No arXiv results found for: {query}"
            
        return "\n\n".join(results)
        
    except Exception as e:
        return f"An error occurred while querying arXiv: {str(e)}"


@tool
def search_wikipedia(topic: str, language: str = "en") -> str:
    """Search Wikipedia for a `topic` on given `language` and return a summary of the article."""
    try:
        wk.set_lang(language)
        page = wk.page(topic, auto_suggest=False)
        return page.summary
    except Exception as E:
        return f"Error while searching wikipedia: {str(E)}"

