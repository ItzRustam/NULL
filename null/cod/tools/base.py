# Author: ItzRustam (Rustam Singh Bhadouriya)
# Project: NULL Multi-Agent Ecosystem | Licensed under the MIT License

"""This File Contains Tools (abilities) For COD"""


from langchain_core.tools import tool
import sys
from pathlib import Path
from typing import Union, Tuple

WORKSPACE = Path("./agent_workspace")
WORKSPACE.mkdir(exist_ok=True)

import subprocess

def resolve_safe_path(filepath: str) -> Tuple[Union[Path, None], Union[str, None]]:
    try:
        resolved_workspace = WORKSPACE.resolve()
        target = (resolved_workspace / filepath).resolve()

        if not target.is_relative_to(resolved_workspace):
            return None, f"Error: Access denied. '{filepath}' attempts path traversal."

        return target, None
    except Exception as e:
        return None, f"Error: Failed to resolve path '{filepath}'. Details: {str(e)}"

@tool
def create_folder(path: str) -> str:
    """
    Creates a new directory inside the workspace.
    
    Args:
        path (str): The relative path of the directory to create.
        
    Returns:
        str: Status message indicating success, warning, or error details.
    """
    task_path, err = resolve_safe_path(path)
    if err:
        return err

    try:
        if task_path.exists() and task_path.is_dir():
            return f"Warning: Directory '{path}' already exists."

        task_path.mkdir(parents=True, exist_ok=True)
        return f"Success: Directory '{path}' created successfully."
    except Exception as e:
        return f"Error: Failed to create directory. Details: {str(e)}"


@tool
def find_file(filename: str) -> Union[bool, str]:
    """
    Checks if a file exists within the workspace.
    
    Args:
        filename (str): The relative path of the file to verify.
        
    Returns:
        bool | str: True if the file exists, False if not found, or an error string if path resolution fails.
    """
    file_path, err = resolve_safe_path(filename)
    if err:
        return err

    try:
        return file_path.exists() and file_path.is_file()
    except Exception as e:
        return f"Error: Failed to find file. Details: {str(e)}"
    

@tool
def run_python_code(filename: str) -> str:
    """
    Executes a specified Python script located inside the workspace and returns its output.
    
    Args:
        filename (str): The exact name of the Python file to run (e.g., 'script.py' or 'src/test.py').
        
    Returns:
        str: The standard output (stdout) and standard error (stderr) of the script.
    """
    file_path, err = resolve_safe_path(filename)
    if err:
        return err

    if not file_path.exists():
        return f"Error: File not found at {filename}"

    if not file_path.is_file():
        return f"Error: {filename} is a directory, not a python file."

    try:
        result = subprocess.run(
            [sys.executable, str(file_path)],
            capture_output=True,
            text=True,
        )

        output = result.stdout
        if result.stderr:
            output += f"\n[STDERR / ERRORS]:\n{result.stderr}"

        return output.strip() if output else "Success: Script ran but produced no console output."

    except subprocess.TimeoutExpired:
        return "Error: Script execution timed out after 30 seconds."
    except Exception as e:
        return f"Error executing script: {str(e)}"


@tool
def read_file(filename: str) -> str:
    """
    Reads and returns the exact text content of a file from the workspace.
    
    Args:
        filename (str): The relative path of the file to read (e.g., 'data.txt' or 'app.py').
        
    Returns:
        str: The complete text content of the file.
    """
    path, err = resolve_safe_path(filename)
    if err:
        return err

    if not path.exists():
        return f"Error: File not found at {filename}"

    if not path.is_file():
        return f"Error: {filename} is a directory, not a file."

    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return f"Error: Cannot read {filename}. It might be a binary file or have an unsupported encoding."
    except Exception as e:
        return f"Error: Failed to read {filename}. Details: {str(e)}"


@tool
def create_file(filename: str, content: str) -> str:
    """
    Creates a new text file or overwrites an existing one in the workspace.
    
    Args:
        filename (str): The relative path to save the file (e.g., 'main.py' or 'logs/info.txt').
        content (str): The exact, complete text to write into the file. leave it to a empty string when no content is given
        
    Returns:
        str: A success message confirming the file path and the size of the data written.
    """
    path, err = resolve_safe_path(filename)
    if err:
        return err

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"Success: Created file '{filename}' and wrote {len(content)} characters."
    except Exception as e:
        return f"Error: Failed to write to {filename}. Details: {str(e)}"


@tool
def get_text_length(text: str) -> int:
    """
    Calculates and returns the exact number of characters in a given string.
    
    Args:
        text (str): The input text string to measure.
        
    Returns:
        int: The total character count.
    """
    return len(text)