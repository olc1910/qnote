#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qnote.commands.list - List Command Implementations

This module implements listing commands for displaying items:
- list_notes: List all notes with filtering
- list_snippets: List code snippets
- list_todos: List TODO items

Copyright (c) 2026 qnote
Licensed under the MIT License.
"""

from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from qnote.core.note import Note
from qnote.core.snippet import Snippet
from qnote.core.todo import Todo
from qnote.utils.formatter import error, info

console = Console()


def list_notes(
    tags: Optional[str] = None,
    limit: int = 50,
    sort_by: str = "updated",
    starred_only: bool = False
) -> None:
    """
    List all notes with optional filtering and sorting.
    
    Displays notes in a formatted table with:
    - ID, title, tags, update time, starred status
    - Color-coded output
    - Pagination support
    
    Args:
        tags: Comma-separated tag filter (e.g., "python,tutorial")
        limit: Maximum number of notes to display (default: 50)
        sort_by: Sort field - created, updated, or title (default: updated)
        starred_only: If True, show only starred notes
    
    Examples:
        >>> list_notes()  # All notes
        >>> list_notes(tags="python")  # Filter by tag
        >>> list_notes(limit=10, starred_only=True)  # Top 10 starred
        >>> list_notes(sort_by="created")  # Sort by creation date
    """
    # Parse tags from comma-separated string
    tag_list: Optional[List[str]] = None
    if tags:
        tag_list = [
            tag.strip().lower() 
            for tag in tags.split(",") 
            if tag.strip()
        ]
    
    # Map CLI sort option to database field
    sort_map = {
        "created": "created_at",
        "updated": "updated_at",
        "title": "title"
    }
    sort_field = sort_map.get(sort_by, "updated_at")
    
    # Fetch notes from database
    try:
        notes = Note.get_all(
            limit=limit,
            tags=tag_list,
            starred_only=starred_only,
            sort_by=sort_field
        )
    except Exception as e:
        error(f"Failed to fetch notes: {e}")
        return
    
    # Handle empty result
    if not notes:
        _show_empty_notes_message(tag_list, starred_only)
        return
    
    # Display results in table
    _display_notes_table(notes, tag_list, starred_only)


def list_snippets(
    language: Optional[str] = None,
    tags: Optional[str] = None,
    limit: int = 50,
    starred_only: bool = False
) -> None:
    """
    List all code snippets with optional filtering.
    
    Args:
        language: Filter by programming language (e.g., "python")
        tags: Comma-separated tag filter
        limit: Maximum number of snippets to display
        starred_only: If True, show only starred snippets
    
    Examples:
        >>> list_snippets()  # All snippets
        >>> list_snippets(language="python")  # Python snippets only
        >>> list_snippets(tags="algorithm")  # By tag
    """
    # Parse tags
    tag_list: Optional[List[str]] = None
    if tags:
        tag_list = [
            tag.strip().lower() 
            for tag in tags.split(",") 
            if tag.strip()
        ]
    
    # Fetch snippets
    try:
        snippets = Snippet.get_all(
            limit=limit,
            language=language.lower() if language else None,
            tags=tag_list,
            starred_only=starred_only
        )
    except Exception as e:
        error(f"Failed to fetch snippets: {e}")
        return
    
    # Handle empty result
    if not snippets:
        _show_empty_snippets_message(language, tag_list, starred_only)
        return
    
    # Display results
    _display_snippets_table(snippets, language, tag_list, starred_only)


def list_todos(
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    tags: Optional[str] = None,
    limit: int = 50,
    overdue_only: bool = False
) -> None:
    """
    List all TODO items with optional filtering.
    
    Args:
        completed: Filter by completion status (None = all)
        priority: Filter by priority level (low, medium, high)
        tags: Comma-separated tag filter
        limit: Maximum number of TODOs to display
        overdue_only: If True, show only overdue TODOs
    
    Examples:
        >>> list_todos()  # All TODOs
        >>> list_todos(completed=False)  # Pending only
        >>> list_todos(priority="high")  # High priority
        >>> list_todos(overdue_only=True)  # Overdue tasks
    """
    # Validate priority if specified
    if priority:
        priority = priority.lower()
        if priority not in ["low", "medium", "high"]:
            error(f"Invalid priority: {priority}")
            console.print("\n[dim]Valid priorities: low, medium, high[/dim]")
            return
    
    # Parse tags
    tag_list: Optional[List[str]] = None
    if tags:
        tag_list = [
            tag.strip().lower() 
            for tag in tags.split(",") 
            if tag.strip()
        ]
    
    # Fetch TODOs
    try:
        todos = Todo.get_all(
            limit=limit,
            completed=completed,
            priority=priority,
            tags=tag_list,
            overdue_only=overdue_only
        )
    except Exception as e:
        error(f"Failed to fetch TODOs: {e}")
        return
    
    # Handle empty result
    if not todos:
        _show_empty_todos_message(completed, priority, tag_list, overdue_only)
        return
    
    # Display results
    _display_todos_table(todos, completed, priority, overdue_only)


# Helper functions for displaying tables

def _display_notes_table(
    notes: List[Note],
    tag_filter: Optional[List[str]] = None,
    starred_only: bool = False
) -> None:
    """
    Display notes in a formatted Rich table.
    
    Args:
        notes: List of Note objects to display
        tag_filter: Applied tag filter (for display)
        starred_only: Whether only starred notes are shown
    """
    # Build title
    title_parts = [f"Notes ({len(notes)} total)"]
    if starred_only:
        title_parts.append("★ Starred")
    if tag_filter:
        title_parts.append(f"Tags: {', '.join(tag_filter)}")
    
    title = " • ".join(title_parts)
    
    # Create table
    table = Table(title=title, show_header=True, header_style="bold cyan")
    
    # Define columns
    table.add_column("ID", style="cyan", justify="right", width=6)
    table.add_column("Title", style="white", width=35, no_wrap=False)
    table.add_column("Tags", style="magenta", width=20)
    table.add_column("Updated", style="green", width=16)
    table.add_column("★", justify="center", width=3)
    
    # Add rows
    for note in notes:
        note_id = str(note.id)
        
        # Use title or truncated content
        if note.title:
            title_text = _truncate(note.title, 35)
        else:
            title_text = _truncate_content(note.content, 35)
        
        # Format tags
        if note.tags:
            tags_text = ", ".join(note.tags[:3])  # Max 3 tags
            if len(note.tags) > 3:
                tags_text += f" +{len(note.tags) - 3}"
        else:
            tags_text = "[dim]-[/dim]"
        
        # Format timestamp
        updated = note.updated_at.strftime("%Y-%m-%d %H:%M") if note.updated_at else "-"
        
        # Star symbol
        star = "★" if note.is_starred else ""
        
        table.add_row(note_id, title_text, tags_text, updated, star)
    
    # Print table
    console.print()
    console.print(table)
    console.print()
    
    # Print helpful tips
    console.print("[dim]Commands:[/dim]")
    console.print("[dim]  qnote show <id>     View note details[/dim]")
    console.print("[dim]  qnote edit <id>     Edit note[/dim]")
    console.print("[dim]  qnote delete <id>   Delete note[/dim]")
    console.print()


def _display_snippets_table(
    snippets: List[Snippet],
    language_filter: Optional[str] = None,
    tag_filter: Optional[List[str]] = None,
    starred_only: bool = False
) -> None:
    """Display snippets in a formatted table."""
    # Build title
    title_parts = [f"Snippets ({len(snippets)} total)"]
    if starred_only:
        title_parts.append("★ Starred")
    if language_filter:
        title_parts.append(f"Language: {language_filter}")
    if tag_filter:
        title_parts.append(f"Tags: {', '.join(tag_filter)}")
    
    title = " • ".join(title_parts)
    
    # Create table
    table = Table(title=title, show_header=True, header_style="bold cyan")
    
    # Define columns
    table.add_column("ID", style="cyan", justify="right", width=6)
    table.add_column("Title/Description", style="white", width=30)
    table.add_column("Lang", style="yellow", width=10)
    table.add_column("Lines", style="blue", justify="right", width=6)
    table.add_column("Tags", style="magenta", width=18)
    table.add_column("★", justify="center", width=3)
    
    # Add rows
    for snippet in snippets:
        snippet_id = str(snippet.id)
        
        # Title or description
        if snippet.title:
            title_text = _truncate(snippet.title, 30)
        elif snippet.description:
            title_text = _truncate(snippet.description, 30)
        else:
            # Use first line of code
            first_line = snippet.code.split('\n')[0]
            title_text = _truncate(first_line, 30)
        
        # Language
        lang = snippet.language or "[dim]?[/dim]"
        
        # Line count
        lines = str(len(snippet.code.splitlines()))
        
        # Tags
        if snippet.tags:
            tags_text = ", ".join(snippet.tags[:2])
            if len(snippet.tags) > 2:
                tags_text += f" +{len(snippet.tags) - 2}"
        else:
            tags_text = "[dim]-[/dim]"
        
        # Star
        star = "★" if snippet.is_starred else ""
        
        table.add_row(snippet_id, title_text, lang, lines, tags_text, star)
    
    # Print
    console.print()
    console.print(table)
    console.print()
    
    console.print("[dim]Commands:[/dim]")
    console.print("[dim]  qnote snippet show <id>   View snippet with syntax highlighting[/dim]")
    console.print("[dim]  qnote snippet copy <id>   Copy to clipboard[/dim]")
    console.print()


def _display_todos_table(
    todos: List[Todo],
    completed_filter: Optional[bool],
    priority_filter: Optional[str],
    overdue_only: bool
) -> None:
    """Display TODOs in a formatted table."""
    # Build title
    title_parts = [f"TODOs ({len(todos)} total)"]
    if completed_filter is True:
        title_parts.append("✓ Completed")
    elif completed_filter is False:
        title_parts.append("☐ Pending")
    if priority_filter:
        title_parts.append(f"Priority: {priority_filter.upper()}")
    if overdue_only:
        title_parts.append("⚠ Overdue")
    
    title = " • ".join(title_parts)
    
    # Create table
    table = Table(title=title, show_header=True, header_style="bold cyan")
    
    # Define columns
    table.add_column("", width=2)  # Checkbox
    table.add_column("ID", style="cyan", justify="right", width=5)
    table.add_column("Title", style="white", width=35)
    table.add_column("Priority", width=8)
    table.add_column("Due Date", style="green", width=12)
    table.add_column("Tags", style="magenta", width=15)
    
    # Add rows
    for todo in todos:
        # Checkbox
        checkbox = "✓" if todo.completed else "☐"
        
        # ID
        todo_id = str(todo.id)
        
        # Title (strikethrough if completed)
        title = _truncate(todo.title, 35)
        if todo.completed:
            title = f"[dim strikethrough]{title}[/dim strikethrough]"
        
        # Priority with color
        priority_colors = {
            "low": "green",
            "medium": "yellow",
            "high": "red"
        }
        priority_color = priority_colors.get(todo.priority, "white")
        priority_text = f"[{priority_color}]{todo.priority.upper()}[/{priority_color}]"
        
        # Due date
        if todo.due_date:
            due_str = todo.due_date.strftime('%Y-%m-%d')
            if todo.is_overdue:
                due_text = f"[bold red]{due_str}[/bold red]"
            else:
                due_text = due_str
        else:
            due_text = "[dim]-[/dim]"
        
        # Tags
        if todo.tags:
            tags_text = ", ".join(todo.tags[:2])
            if len(todo.tags) > 2:
                tags_text += f" +{len(todo.tags) - 2}"
        else:
            tags_text = "[dim]-[/dim]"
        
        table.add_row(checkbox, todo_id, title, priority_text, due_text, tags_text)
    
    # Print
    console.print()
    console.print(table)
    console.print()
    
    # Statistics
    completed_count = sum(1 for t in todos if t.completed)
    pending_count = len(todos) - completed_count
    overdue_count = sum(1 for t in todos if t.is_overdue)
    
    stats = f"[dim]Completed: {completed_count} • Pending: {pending_count}"
    if overdue_count > 0:
        stats += f" • [red]Overdue: {overdue_count}[/red]"
    stats += "[/dim]"
    console.print(stats)
    console.print()
    
    console.print("[dim]Commands:[/dim]")
    console.print("[dim]  qnote todo done <id>     Mark as completed[/dim]")
    console.print("[dim]  qnote todo show <id>     View TODO details[/dim]")
    console.print()


# Helper functions for empty messages

def _show_empty_notes_message(
    tag_filter: Optional[List[str]],
    starred_only: bool
) -> None:
    """Show helpful message when no notes are found."""
    console.print()
    
    if tag_filter:
        info(f"No notes found with tags: {', '.join(tag_filter)}")
        console.print("\n[dim]Try:[/dim]")
        console.print("[dim]  qnote list              List all notes[/dim]")
        console.print("[dim]  qnote list --tags other Remove filter[/dim]")
    elif starred_only:
        info("No starred notes found")
        console.print("\n[dim]Star a note with:[/dim]")
        console.print("[dim]  qnote star <id>[/dim]")
    else:
        info("No notes found. Create your first note!")
        console.print("\n[dim]Get started:[/dim]")
        console.print("[dim]  qnote add \"My first note\"[/dim]")
        console.print("[dim]  qnote add --editor[/dim]")
    
    console.print()


def _show_empty_snippets_message(
    language_filter: Optional[str],
    tag_filter: Optional[List[str]],
    starred_only: bool
) -> None:
    """Show helpful message when no snippets are found."""
    console.print()
    
    if language_filter or tag_filter:
        info("No snippets found with specified filters")
        console.print("\n[dim]Try:[/dim]")
        console.print("[dim]  qnote snippet list      List all snippets[/dim]")
    elif starred_only:
        info("No starred snippets found")
    else:
        info("No snippets found. Create your first snippet!")
        console.print("\n[dim]Get started:[/dim]")
        console.print("[dim]  qnote snippet add \"code\" -l python[/dim]")
        console.print("[dim]  qnote snippet add --from-file script.py[/dim]")
    
    console.print()


def _show_empty_todos_message(
    completed_filter: Optional[bool],
    priority_filter: Optional[str],
    tag_filter: Optional[List[str]],
    overdue_only: bool
) -> None:
    """Show helpful message when no TODOs are found."""
    console.print()
    
    if overdue_only:
        info("No overdue TODOs! 🎉")
        console.print("\n[dim]Great job staying on top of things![/dim]")
    elif completed_filter or priority_filter or tag_filter:
        info("No TODOs found with specified filters")
        console.print("\n[dim]Try:[/dim]")
        console.print("[dim]  qnote todo list         List all TODOs[/dim]")
    else:
        info("No TODOs found. Create your first task!")
        console.print("\n[dim]Get started:[/dim]")
        console.print("[dim]  qnote todo add \"My task\"[/dim]")
        console.print("[dim]  qnote todo add \"Important\" -p high[/dim]")
    
    console.print()


# Utility functions

def _truncate(text: str, max_length: int) -> str:
    """
    Truncate text to max length, adding ellipsis if needed.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
    
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def _truncate_content(content: str, max_length: int) -> str:
    """
    Truncate multi-line content to a single line.
    
    Args:
        content: Content to truncate
        max_length: Maximum length
    
    Returns:
        Truncated single-line string
    """
    # Remove newlines and extra whitespace
    single_line = " ".join(content.split())
    return _truncate(single_line, max_length)
