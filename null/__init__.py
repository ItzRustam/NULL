# Author: ItzRustam (Rustam Singh Bhadouriya)
# Project: NULL Multi-Agent Ecosystem | Licensed under the MIT License

"""
NULL Multi-Agent Ecosystem - Parsers Module

Exports all parser classes, SafeParser, and LangChain Pydantic parsers
for the NULL Multi-Agent Ecosystem.
"""

from .parsers import (
    # Pydantic Models
    NullOutput,
    CodOutput,
    TechnoOutput,
    AlexOutput,
    CoreXOutput,
    CodeSecurityAudit,

    # SafeParser Class
    SafeParser,

    # LangChain Pydantic Output Parsers
    null_parser,
    cod_parser,
    alex_parser,
    techno_parser,
    corex_parser,
    john_parser,
)
from .prompts import (
    null_system_prompt,
    cod_system_prompt,
    john_system_message,
    techno_system_prompt
)

# Agents
from . import (
    techno,
    cod,

    # Head Agent
    null
)


__all__ = [
    # Pydantic Models
    "NullOutput",
    "CodOutput",
    "TechnoOutput",
    "AlexOutput",
    "CoreXOutput",

    # SafeParser Class
    "SafeParser",

    # LangChain Pydantic Output Parsers
    "null_parser",
    "cod_parser",
    "alex_parser",
    "techno_parser",
    "corex_parser",

    # system prompts
    "null_system_prompt",
    "cod_system_prompt",
    "john_system_message",
    "techno_system_prompt",

    # Agents
    "techno",
    "cod",

    # Head Agent
    "null"
]