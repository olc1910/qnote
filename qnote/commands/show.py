#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qnote.commands.show - Show Command Implementations

Display single items with full formatting and details.

Copyright (c) 2026 qnote
Licensed under the MIT License.
"""

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax

from qnote.core.note import Note
from qnote.core.snippet import Snippet
from qnote.core.todo import Todo
from qnote.utils.formatter import error

console = Console()


def show_note(note_id: int) -> None:
    """
    Display a note by ID with full formatting.
    
    Args:
        note_id: Note ID to display
    
    Examples:
        >>> show_note(42)
    """
    # Fetch note
    note = Note.get_by_id(note_id)
    
    if not note:
        error(f"Note #{note_id} not found")
        console.print("\n[dim]Tip: Use 'qnote list' to see all notes[/dim]")
        return
    
    # Create title
    star = "★" if note.is_starred else "☆"
    title = note.title if note.title else f"Note #{note.id}"
    header = f"{star} {title}"
    
    # Create metadata
    metadata_lines = []
    metadata_lines.append(f"[cyan]ID:[/cyan] {note.id}")
    metadata_lines.append(f"[cyan]Created:[/cyan] {note.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    metadata_lines.append(f"[cyan]Updated:[/cyan] {note.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if note.tags:
        tags_str = ", ".join(f"[magenta]{tag}[/magenta]" for tag in note.tags)
        metadata_lines.append(f"[cyan]Tags:[/cyan] {tags_str}")
    
    metadata = "\n".join(metadata_lines)
    
    # Display
    console.print()
    console.print(Panel(metadata, title=header, border_style="cyan"))
    console.print()
    
    # Render content as Markdown
    try:
        md = Markdown(note.content)
        console.print(md)
    except Exception:
        # Fallback to plain text if Markdown fails
        console.print(note.content)
    
    console.print()
    console.print("[dim]Commands:[/dim]")
    console.print(f"[dim]  qnote edit {note_id}     Edit this note[/dim]")
    console.print(f"[dim]  qnote delete {note_id}   Delete this note[/dim]")
    console.print()


def show_snippet(snippet_id: int) -> None:
    """
    Display a code snippet with syntax highlighting.
    
    Args:
        snippet_id: Snippet ID to display
    """
    # Fetch snippet
    snippet = Snippet.get_by_id(snippet_id)
    
    if not snippet:
        error(f"Snippet #{snippet_id} not found")
        console.print("\n[dim]Tip: Use 'qnote snippet list' to see all snippets[/dim]")
        return
    
    # Create title
    star = "★" if snippet.is_starred else "☆"
    title = snippet.title if snippet.title else f"Snippet #{snippet.id}"
    header = f"{star} {title}"
    
    # Create metadata
    metadata_lines = []
    metadata_lines.append(f"[cyan]ID:[/cyan] {snippet.id}")
    metadata_lines.append(f"[cyan]Language:[/cyan] {snippet.language or 'unknown'}")
    metadata_lines.append(f"[cyan]Lines:[/cyan] {len(snippet.code.splitlines())}")
    
    if snippet.description:
        metadata_lines.append(f"[cyan]Description:[/cyan] {snippet.description}")
    
    if snippet.tags:
        tags_str = ", ".join(f"[magenta]{tag}[/magenta]" for tag in snippet.tags)
        metadata_lines.append(f"[cyan]Tags:[/cyan] {tags_str}")
    
    metadata_lines.append(f"[cyan]Created:[/cyan] {snippet.created_at.strftime('%Y-%m-%d %H:%M')}")
    
    metadata = "\n".join(metadata_lines)
    
    # Display
    console.print()
    console.print(Panel(metadata, title=header, border_style="cyan"))
    console.print()
    
    # Syntax highlighting
    if snippet.language:
        try:
            syntax = Syntax(
                snippet.code,
                snippet.language,
                theme="monokai",
                line_numbers=True,
                word_wrap=False
            )
            console.print(syntax)
        except Exception:
            # Fallback to plain text
            console.print(snippet.code)
    else:
        console.print(snippet.code)
    
    console.print()
    console.print("[dim]Commands:[/dim]")
    console.print(f"[dim]  qnote snippet copy {snippet_id}   Copy to clipboard[/dim]")
    console.print(f"[dim]  qnote snippet delete {snippet_id} Delete this snippet[/dim]")
    console.print()


def show_todo(todo_id: int) -> None:
    """
    Display a TODO item with full details.
    
    Args:
        todo_id: TODO ID to display
    """
    # Fetch TODO
    todo = Todo.get_by_id(todo_id)
    
    if not todo:
        error(f"TODO #{todo_id} not found")
        console.print("\n[dim]Tip: Use 'qnote todo list' to see all TODOs[/dim]")
        return
    
    # Status symbol
    checkbox = "✓" if todo.completed else "☐"
    
    # Priority color
    priority_colors = {
        "low": "green",
        "medium": "yellow",
        "high": "red"
    }
    priority_color = priority_colors.get(todo.priority, "white")
    
    # Create title
    title = f"{checkbox} {todo.title}"
    if todo.completed:
        title = f"[dim strikethrough]{title}[/dim strikethrough]"
    
    # Create metadata
    metadata_lines = []
    metadata_lines.append(f"[cyan]ID:[/cyan] {todo.id}")
    
    if todo.completed:
        metadata_lines.append(f"[cyan]Status:[/cyan] [green]✓ Completed[/green]")
    else:
        metadata_lines.append(f"[cyan]Status:[/cyan] [yellow]☐ Pending[/yellow]")
    
    metadata_lines.append(f"[cyan]Priority:[/cyan] [{priority_color}]{todo.priority.upper()}[/{priority_color}]")
    
    if todo.due_date:
        due_str = todo.due_date.strftime('%Y-%m-%d')
        if todo.is_overdue and not todo.completed:
            metadata_lines.append(f"[cyan]Due:[/cyan] [bold red]{due_str} (OVERDUE!)[/bold red]")
        else:
            metadata_lines.append(f"[cyan]Due:[/cyan] {due_str}")
    
    if todo.tags:
        tags_str = ", ".join(f"[magenta]{tag}[/magenta]" for tag in todo.tags)
        metadata_lines.append(f"[cyan]Tags:[/cyan] {tags_str}")
    
    metadata_lines.append(f"[cyan]Created:[/cyan] {todo.created_at.strftime('%Y-%m-%d %H:%M')}")
    metadata_lines.append(f"[cyan]Updated:[/cyan] {todo.updated_at.strftime('%Y-%m-%d %H:%M')}")
    
    metadata = "\n".join(metadata_lines)
    
    # Display
    console.print()
    console.print(Panel(metadata, title=title, border_style="cyan"))
    
    if todo.description:
        console.print()
        console.print("[cyan]Description:[/cyan]")
        console.print(todo.description)
    
    console.print()
    console.print("[dim]Commands:[/dim]")
    if not todo.completed:
        console.print(f"[dim]  qnote todo done {todo_id}     Mark as completed[/dim]")
    else:
        console.print(f"[dim]  qnote todo undone {todo_id}   Mark as pending[/dim]")
    console.print(f"[dim]  qnote todo delete {todo_id}   Delete this TODO[/dim]")
    console.print()
