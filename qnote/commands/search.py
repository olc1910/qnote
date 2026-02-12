#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qnote.commands.search - Search Command Implementation

Search across notes, snippets, and TODOs.

Copyright (c) 2026 qnote
Licensed under the MIT License.
"""

from typing import Optional, List
from rich.console import Console
from rich.table import Table

from qnote.core.note import Note
from qnote.core.snippet import Snippet
from qnote.core.todo import Todo
from qnote.utils.formatter import error, info

console = Console()


def search_all(
    query: str,
    item_type: str = "all",
    tags: Optional[str] = None,
    limit: int = 50
) -> None:
    """
    Search through all notes, snippets, and TODOs.
    
    Args:
        query: Search query string
        item_type: Type of items to search (note, snippet, todo, all)
        tags: Optional comma-separated tags filter
        limit: Maximum results per type
    
    Examples:
        >>> search_all("python")
        >>> search_all("function", item_type="snippet")
        >>> search_all("bug", tags="urgent")
    """
    if not query.strip():
        error("Search query cannot be empty")
        return
    
    # Parse tags
    tag_list: Optional[List[str]] = None
    if tags:
        tag_list = [tag.strip().lower() for tag in tags.split(",") if tag.strip()]
    
    # Search based on type
    if item_type in ["all", "note"]:
        search_notes(query, tag_list, limit)
    
    if item_type in ["all", "snippet"]:
        search_snippets(query, tag_list, limit)
    
    if item_type in ["all", "todo"]:
        search_todos(query, tag_list, limit)


def search_notes(query: str, tags: Optional[List[str]] = None, limit: int = 50) -> None:
    """Search notes and display results."""
    try:
        notes = Note.search(query, tags)
        
        if limit and len(notes) > limit:
            notes = notes[:limit]
        
        if not notes:
            if tags:
                console.print(f"\n[yellow]No notes found for '{query}' with tags: {', '.join(tags)}[/yellow]")
            else:
                console.print(f"\n[yellow]No notes found for '{query}'[/yellow]")
            return
        
        # Display results
        console.print(f"\n[bold cyan]Notes ({len(notes)} found)[/bold cyan]")
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("ID", style="cyan", justify="right", width=6)
        table.add_column("Title", style="white", width=30)
        table.add_column("Preview", style="dim", width=50)
        table.add_column("Tags", style="magenta", width=20)
        
        for note in notes:
            note_id = str(note.id)
            title = note.title or "[dim]Untitled[/dim]"
            
            # Create preview with highlighted query
            content_lower = note.content.lower()
            query_lower = query.lower()
            
            if query_lower in content_lower:
                idx = content_lower.find(query_lower)
                start = max(0, idx - 20)
                end = min(len(note.content), idx + len(query) + 30)
                preview = note.content[start:end].replace('\n', ' ')
                if start > 0:
                    preview = "..." + preview
                if end < len(note.content):
                    preview = preview + "..."
            else:
                preview = note.content[:50].replace('\n', ' ') + "..."
            
            tags_str = ", ".join(note.tags[:2]) if note.tags else "-"
            if len(note.tags) > 2:
                tags_str += f" +{len(note.tags) - 2}"
            
            table.add_row(note_id, title, preview, tags_str)
        
        console.print(table)
        console.print()
        
    except Exception as e:
        error(f"Search failed: {e}")


def search_snippets(query: str, tags: Optional[List[str]] = None, limit: int = 50) -> None:
    """Search code snippets and display results."""
    try:
        # Get all snippets first, then filter
        # TODO: Implement proper search in Snippet model
        all_snippets = Snippet.get_all(tags=tags)
        
        # Filter by query
        query_lower = query.lower()
        snippets = [
            s for s in all_snippets
            if query_lower in s.code.lower()
            or (s.title and query_lower in s.title.lower())
            or (s.description and query_lower in s.description.lower())
        ]
        
        if limit and len(snippets) > limit:
            snippets = snippets[:limit]
        
        if not snippets:
            if tags:
                console.print(f"\n[yellow]No snippets found for '{query}' with tags: {', '.join(tags)}[/yellow]")
            else:
                console.print(f"\n[yellow]No snippets found for '{query}'[/yellow]")
            return
        
        # Display results
        console.print(f"\n[bold cyan]Snippets ({len(snippets)} found)[/bold cyan]")
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("ID", style="cyan", justify="right", width=6)
        table.add_column("Title", style="white", width=25)
        table.add_column("Language", style="yellow", width=10)
        table.add_column("Preview", style="dim", width=45)
        
        for snippet in snippets:
            snippet_id = str(snippet.id)
            title = snippet.title or "[dim]Untitled[/dim]"
            lang = snippet.language or "-"
            
            # Create preview
            code_lines = snippet.code.split('\n')
            preview = code_lines[0][:45]
            if len(code_lines) > 1 or len(snippet.code) > 45:
                preview += "..."
            
            table.add_row(snippet_id, title, lang, preview)
        
        console.print(table)
        console.print()
        
    except Exception as e:
        error(f"Search failed: {e}")


def search_todos(query: str, tags: Optional[List[str]] = None, limit: int = 50) -> None:
    """Search TODOs and display results."""
    try:
        # Get all TODOs first, then filter
        # TODO: Implement proper search in Todo model
        all_todos = Todo.get_all(tags=tags)
        
        # Filter by query
        query_lower = query.lower()
        todos = [
            t for t in all_todos
            if query_lower in t.title.lower()
            or (t.description and query_lower in t.description.lower())
        ]
        
        if limit and len(todos) > limit:
            todos = todos[:limit]
        
        if not todos:
            if tags:
                console.print(f"\n[yellow]No TODOs found for '{query}' with tags: {', '.join(tags)}[/yellow]")
            else:
                console.print(f"\n[yellow]No TODOs found for '{query}'[/yellow]")
            return
        
        # Display results
        console.print(f"\n[bold cyan]TODOs ({len(todos)} found)[/bold cyan]")
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("", width=2)
        table.add_column("ID", style="cyan", justify="right", width=6)
        table.add_column("Title", style="white", width=40)
        table.add_column("Priority", width=8)
        table.add_column("Due", style="green", width=12)
        
        for todo in todos:
            checkbox = "✓" if todo.completed else "☐"
            todo_id = str(todo.id)
            title = todo.title
            
            priority_colors = {"low": "green", "medium": "yellow", "high": "red"}
            priority_color = priority_colors.get(todo.priority, "white")
            priority_text = f"[{priority_color}]{todo.priority.upper()}[/{priority_color}]"
            
            due_text = "-"
            if todo.due_date:
                due_text = todo.due_date.strftime('%Y-%m-%d')
                if todo.is_overdue and not todo.completed:
                    due_text = f"[red]{due_text}[/red]"
            
            table.add_row(checkbox, todo_id, title, priority_text, due_text)
        
        console.print(table)
        console.print()
        
    except Exception as e:
        error(f"Search failed: {e}")
