# Author: ItzRustam (Rustam Singh Bhadouriya)
# Project: NULL Multi-Agent Ecosystem | Licensed under the MIT License

from langchain_core.tools import tool
import requests as rq
from typing import Dict, Tuple, Any

@tool
def call_api(url : str, Data : dict, method : str = "get") -> Tuple[int, Dict[Any, Any]]:
    """
    Send an HTTP request to the specified API URL with the provided data.
    Only Support for RSRoute API key.

    Args:
        url: The URL of the API endpoint to call.
        Data: Query parameters or request data to send with the request.
            Do not include keys whose values are None or NULL. Remove
            those keys from the dictionary before making the request.
        method: HTTP method to use. Supported methods are "get" and "post".
            Defaults to "get".

    Returns:
        A tuple containing the HTTP status code and the API response as a
        dictionary.

    Notes:
        Returns an error message when the request fails or an unsupported
        HTTP method is provided.
    """
    
    if method == "get":
        try:
            response = rq.get(url=url, params=Data)
            return response.status_code, response.json()
        except Exception as E:
            return 500, {"Error": str(E)}
    elif method == "post":
        try:
            response = rq.post(url=url, params=Data)
            return response.status_code, response.json()
        except Exception as E:
            return 500, {"Error": str(E)}
    else:
        return "Unsupported Method, Tool only supports `get`, `post`"