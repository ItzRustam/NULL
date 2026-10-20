#!/usr/bin/env python3
# Author: ItzRustam (Rustam Singh Bhadouriya)
# Project: NULL Multi-Agent Ecosystem | Licensed under the MIT License

"""
Interactive CLI for the NULL Multi-Agent Ecosystem.
Provides a rich, aesthetic terminal interface powered by NULL (Head Orchestrator).
"""

import sys
import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.rule import Rule
from rich.text import Text
from rich import box

from null.null import run_null
from null.parsers import NullOutput

console = Console()

def print_banner():
    """Display an aesthetic welcome banner for the NULL Multi-Agent Ecosystem."""
    banner_text = Text()
    banner_text.append(" ███╗   ██╗██╗   ██╗██╗     ██╗     \n", style="bold cyan")
    banner_text.append(" ████╗  ██║██║   ██║██║     ██║     \n", style="bold bright_cyan")
    banner_text.append(" ██╔██╗ ██║██║   ██║██║     ██║     \n", style="bold blue")
    banner_text.append(" ██║╚██╗██║██║   ██║██║     ██║     \n", style="bold bright_magenta")
    banner_text.append(" ██║ ╚████║╚██████╔╝███████╗███████╗\n", style="bold magenta")
    banner_text.append(" ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝\n", style="bold purple")
    banner_text.append("     MULTI-AGENT ECOSYSTEM v2.0     ", style="bold yellow")

    info_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
    info_table.add_column("Agent", style="bold bright_cyan", width=14)
    info_table.add_column("Role", style="white")

    info_table.add_row("🧠 [bold magenta]NULL[/bold magenta]", "Head Orchestrator (Routes tasks, synthesizes outputs)")
    info_table.add_row("📁 [bold green]COD[/bold green]", "File System & Safe Script Execution Manager")
    info_table.add_row("🌐 [bold yellow]TECHNO[/bold yellow]", "API & Network Integration Gateway Manager")
    info_table.add_row("🔍 [bold blue]ALEX[/bold blue]", "Deep Researcher (Web, Wikipedia, ArXiv)")
    info_table.add_row("💻 [bold red]COREX[/bold red]", "Code Generation, Logic & Software Structuring")

    content = Table.grid(padding=1)
    content.add_column(justify="center")
    content.add_row(banner_text)
    content.add_row(Rule(style="dim cyan"))
    content.add_row(info_table)
    content.add_row(Rule(style="dim cyan"))
    content.add_row(
        Text(
            "Commands: Type 'exit' or 'leave' to quit | 'clear' to reset screen | 'help' for info",
            style="italic dim yellow",
        )
    )

    console.print(
        Panel(
            content,
            border_style="bright_cyan",
            box=box.DOUBLE,
            padding=(1, 2),
            title="[bold bright_white on blue] ✦ NULL CONSOLE INTERFACE ✦ [/bold bright_white on blue]",
            subtitle="[dim]Powered by LangChain & Gemini[/dim]",
        )
    )


def print_help():
    """Print help information and example workflows."""
    help_table = Table(
        title="💡 Sub-Agents & Example Workflows",
        box=box.ROUNDED,
        header_style="bold cyan",
        border_style="dim cyan",
    )
    help_table.add_column("Agent", style="bold yellow", width=12)
    help_table.add_column("Specialty", style="white", width=25)
    help_table.add_column("Sample Prompt", style="italic green")

    help_table.add_row(
        "Alex",
        "Web & Paper Research",
        "Search the web for the latest Python 3.13 features",
    )
    help_table.add_row(
        "Cod",
        "File Operations & Run",
        "Create a script test.py that prints hello and run it",
    )
    help_table.add_row(
        "Techno",
        "API Requests",
        "Send a GET request to the gateway endpoint",
    )
    help_table.add_row(
        "CoreX",
        "Code Generation",
        "Write a Python function to sort a list using quicksort",
    )
    help_table.add_row(
        "Full Team",
        "Multi-Step Orchestration",
        "Research quantum computing basics and save summary to qc.txt",
    )

    console.print(help_table)


def display_final_response(response):
    """
    Render the final response from NULL with high visual attention,
    rich typography, status badges, and syntax-highlighted markdown.
    """
    timestamp = datetime.now().strftime("%H:%M:%S")

    if isinstance(response, NullOutput):
        status_color = "bright_green" if response.status.lower() == "success" else "yellow"
        if "error" in response.status.lower() or "fail" in response.status.lower():
            status_color = "bright_red"

        header_grid = Table.grid(expand=True)
        header_grid.add_column(justify="left")
        header_grid.add_column(justify="right")
        header_grid.add_row(
            f"[{status_color}]● Workflow Status: [bold]{response.status}[/bold][/{status_color}]",
            f"[dim cyan]Completed at {timestamp}[/dim cyan]",
        )

        md_content = Markdown(response.response)

        panel_content = Table.grid(padding=1, expand=True)
        panel_content.add_column()
        panel_content.add_row(header_grid)
        panel_content.add_row(Rule(style=f"dim {status_color}"))
        panel_content.add_row(md_content)

        console.print()
        console.print(
            Rule(
                f"[bold {status_color}]✨ ═══════════════ FINAL RESPONSE FROM NULL ═══════════════ ✨[/bold {status_color}]",
                style=status_color,
            )
        )
        console.print(
            Panel(
                panel_content,
                box=box.HEAVY,
                border_style=f"bold {status_color}",
                padding=(1, 2),
                title="[bold bright_white on dark_blue] 🤖 NULL HEAD ORCHESTRATOR [/bold bright_white on dark_blue]",
                subtitle=f"[{status_color}]Status: {response.status} • Completed[/{status_color}]",
            )
        )
        console.print(Rule(style=f"dim {status_color}"))
        console.print()

    elif isinstance(response, str):
        is_error = "error" in response.lower() or "denied" in response.lower()
        border_col = "bright_red" if is_error else "bright_blue"
        title_badge = (
            "[bold white on dark_red] ⚠️ NOTICE / REFUSAL [/bold white on dark_red]"
            if is_error
            else "[bold white on dark_blue] 💬 RESPONSE [/bold white on dark_blue]"
        )

        console.print()
        console.print(
            Rule(
                f"[bold {border_col}]✨ ═══════════════ FINAL RESPONSE ═══════════════ ✨[/bold {border_col}]",
                style=border_col,
            )
        )
        console.print(
            Panel(
                Markdown(response),
                box=box.ROUNDED,
                border_style=f"bold {border_col}",
                padding=(1, 2),
                title=title_badge,
                subtitle=f"[dim]Time: {timestamp}[/dim]",
            )
        )
        console.print(Rule(style=f"dim {border_col}"))
        console.print()

    else:
        # Fallback for dict or any other unexpected object
        console.print()
        console.print(
            Panel(
                str(response),
                box=box.ROUNDED,
                border_style="bold yellow",
                padding=(1, 2),
                title="[bold yellow]🤖 NULL RAW OUTPUT[/bold yellow]",
            )
        )
        console.print()


def print_goodbye():
    """Print a stylish farewell message when exiting."""
    farewell_text = Text()
    farewell_text.append("\n  👋 ", style="bold bright_yellow")
    farewell_text.append("See You again!\n", style="bold bright_green")
    farewell_text.append("  Thank you for using NULL Multi-Agent Ecosystem.\n", style="dim cyan")

    console.print(
        Panel(
            farewell_text,
            border_style="bright_green",
            box=box.ROUNDED,
            padding=(0, 2),
        )
    )


def main():
    """Main CLI execution loop."""
    console.clear()
    print_banner()

    while True:
        try:
            console.print("[bold bright_cyan]╭─[ User Query ][/bold bright_cyan]")
            query = console.input("[bold bright_cyan]╰─❯ [/bold bright_cyan]").strip()

            if not query:
                continue

            # Check exit conditions
            if query.lower() in ["exit", "leave", "quit", "q"]:
                print_goodbye()
                break

            if query.lower() in ["clear", "cls"]:
                console.clear()
                print_banner()
                continue

            if query.lower() in ["help", "?"]:
                print_help()
                continue

            # Notify user that NULL orchestration is starting
            console.print()
            console.print(
                Rule(
                    "[bold yellow]⚙️ NULL Orchestrating Tasks Across Agents...[/bold yellow]",
                    style="yellow",
                )
            )

            # Run NULL agent
            response = run_null(query=query)

            # Render final output with maximum visual attention
            display_final_response(response)

        except (KeyboardInterrupt, EOFError):
            console.print()
            print_goodbye()
            break
        except Exception as e:
            console.print(
                Panel(
                    f"[bold red]Unexpected CLI Error:[/bold red] {str(e)}",
                    border_style="red",
                    box=box.ROUNDED,
                )
            )


if __name__ == "__main__":
    main()
