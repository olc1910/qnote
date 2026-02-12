#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qnote.utils.formatter - Output Formatting

This module provides formatting utilities for terminal output using Rich.
Handles:
- Syntax highlighting for code snippets
- Markdown rendering
- Tables for list views
- Progress indicators
- Color themes

Copyright (c) 2026 Otis L. Crossley
Licensed under the MIT License.
"""

from typing import List, Optional
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.panel import Panel
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.util import ClassNotFound


# Global console instance
console = Console()


def print_note(note_id: int, title: Optional[str], content: str, 
               tags: List[str], created_at: datetime, updated_at: datetime,
               is_starred: bool) -> None:
    """
    Print a note with formatting.
    
    Args:
        note_id: Note ID
        title: Note title (optional)
        content: Note content (Markdown)
        tags: List of tags
        created_at: Creation timestamp
        updated_at: Last update timestamp
        is_starred: Starred status
    
    TODO: Implement rich formatting with panels and markdown rendering
    """
    # Placeholder implementation
    star = "★" if is_starred else "☆"
    header = f"[bold]{star} Note #{note_id}[/bold]"
    if title:
        header += f": {title}"
    
    console.print(header)
    console.print(f"Tags: {', '.join(tags) if tags else 'None'}")
    console.print(f"Created: {created_at.strftime('%Y-%m-%d %H:%M')}")
    console.print(f"Updated: {updated_at.strftime('%Y-%m-%d %H:%M')}")
    console.print()
    
    # Render Markdown content
    md = Markdown(content)
    console.print(md)


def print_snippet(snippet_id: int, title: Optional[str], code: str,
                  language: Optional[str], description: Optional[str],
                  tags: List[str], is_starred: bool) -> None:
    """
    Print a code snippet with syntax highlighting.
    
    Args:
        snippet_id: Snippet ID
        title: Snippet title
        code: Code content
        language: Programming language
        description: Optional description
        tags: List of tags
        is_starred: Starred status
    
    TODO: Implement with Rich Syntax highlighting
    """
    star = "★" if is_starred else "☆"
    header = f"[bold]{star} Snippet #{snippet_id}[/bold]"
    if title:
        header += f": {title}"
    
    console.print(header)
    if description:
        console.print(description)
    console.print(f"Language: {language or 'unknown'}")
    console.print(f"Tags: {', '.join(tags) if tags else 'None'}")
    console.print()
    
    # Syntax highlighting
    if language:
        try:
            syntax = Syntax(code, language, theme="monokai", line_numbers=True)
            console.print(syntax)
        except Exception:
            # Fallback to plain text
            console.print(code)
    else:
        console.print(code)


def print_todo(todo_id: int, title: str, description: Optional[str],
               completed: bool, priority: str, due_date: Optional[datetime],
               tags: List[str]) -> None:
    """
    Print a TODO item.
    
    Args:
        todo_id: TODO ID
        title: TODO title
        description: Optional description
        completed: Completion status
        priority: Priority level
        due_date: Due date
        tags: List of tags
    
    TODO: Implement with Rich formatting and priority indicators
    """
    checkbox = "✓" if completed else "☐"
    
    # Priority indicators
    priority_colors = {
        "low": "green",
        "medium": "yellow",
        "high": "red"
    }
    priority_color = priority_colors.get(priority, "white")
    
    console.print(f"{checkbox} [bold]TODO #{todo_id}[/bold]: {title}")
    console.print(f"Priority: [{priority_color}]{priority.upper()}[/{priority_color}]")
    
    if description:
        console.print(f"Description: {description}")
    
    if due_date:
        due_str = due_date.strftime('%Y-%m-%d')
        is_overdue = not completed and datetime.now() > due_date
        if is_overdue:
            console.print(f"Due: [bold red]{due_str} (OVERDUE!)[/bold red]")
        else:
            console.print(f"Due: {due_str}")
    
    if tags:
        console.print(f"Tags: {', '.join(tags)}")


def print_notes_table(notes: List[dict]) -> None:
    """
    Print a table of notes.
    
    Args:
        notes: List of note dictionaries with keys: id, title, tags, updated_at, is_starred
    
    TODO: Implement with Rich Table
    """
    if not notes:
        console.print("[yellow]No notes found[/yellow]")
        return
    
    table = Table(title="Notes")
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Title", style="white")
    table.add_column("Tags", style="magenta")
    table.add_column("Updated", style="green")
    table.add_column("★", justify="center")
    
    for note in notes:
        star = "★" if note.get("is_starred") else ""
        title = note.get("title") or "Untitled"
        tags = ", ".join(note.get("tags", []))
        updated = note.get("updated_at", "")
        if isinstance(updated, datetime):
            updated = updated.strftime("%Y-%m-%d %H:%M")
        
        table.add_row(
            str(note["id"]),
            title,
            tags,
            updated,
            star
        )
    
    console.print(table)


def highlight_code(code: str, language: Optional[str] = None) -> str:
    """
    Highlight code with syntax highlighting.
    
    Args:
        code: Code to highlight
        language: Programming language (if None, tries to guess)
    
    Returns:
        Highlighted code as string
    
    TODO: Implement with Pygments
    """
    # Placeholder
    return code


def render_markdown(text: str) -> None:
    """
    Render Markdown text to terminal.
    
    Args:
        text: Markdown text
    
    TODO: Implement with Rich Markdown
    """
    md = Markdown(text)
    console.print(md)


def error(message: str) -> None:
    """
    Print error message.
    
    Args:
        message: Error message
    """
    console.print(f"[bold red]Error:[/bold red] {message}")


def success(message: str) -> None:
    """
    Print success message.
    
    Args:
        message: Success message
    """
    console.print(f"[bold green]✓[/bold green] {message}")


def warning(message: str) -> None:
    """
    Print warning message.
    
    Args:
        message: Warning message
    """
    console.print(f"[bold yellow]⚠[/bold yellow] {message}")


def info(message: str) -> None:
    """
    Print info message.
    
    Args:
        message: Info message
    """
    console.print(f"[bold blue]ℹ[/bold blue] {message}")
