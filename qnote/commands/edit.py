#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qnote.commands.edit - Edit Command Implementations

Edit existing items in external editor.

Copyright (c) 2026 qnote
Licensed under the MIT License.
"""

from rich.console import Console

from qnote.core.note import Note
from qnote.core.snippet import Snippet
from qnote.core.todo import Todo
from qnote.utils.editor import open_in_editor, EditorError
from qnote.utils.formatter import success, error, warning

console = Console()


def edit_note(note_id: int) -> None:
    """
    Edit a note in external editor.
    
    Args:
        note_id: Note ID to edit
    
    Examples:
        >>> edit_note(42)
    """
    # Fetch note
    note = Note.get_by_id(note_id)
    
    if not note:
        error(f"Note #{note_id} not found")
        console.print("\n[dim]Tip: Use 'qnote list' to see all notes[/dim]")
        return
    
    console.print(f"[cyan]Editing note #{note_id}...[/cyan]")
    if note.title:
        console.print(f"[dim]Title: {note.title}[/dim]")
    
    # Open in editor
    try:
        edited_content = open_in_editor(
            initial_content=note.content,
            extension=".md"
        )
        
        if not edited_content:
            warning("No changes made - content is empty or unchanged")
            return
        
        # Check if actually changed
        if edited_content == note.content:
            console.print("[yellow]No changes made[/yellow]")
            return
        
        # Update note
        note.content = edited_content
        note.save()
        
        success(f"Note #{note_id} updated successfully!")
        
        # Show preview
        preview = edited_content[:100] + "..." if len(edited_content) > 100 else edited_content
        console.print(f"\n[dim]{preview}[/dim]\n")
        
    except EditorError as e:
        error(f"Editor error: {e}")
        console.print("\n[dim]Tip: Configure editor with:[/dim]")
        console.print("[dim]  qnote config set editor vim[/dim]")
    except Exception as e:
        error(f"Failed to update note: {e}")


def edit_snippet(snippet_id: int) -> None:
    """
    Edit a code snippet in external editor.
    
    Args:
        snippet_id: Snippet ID to edit
    """
    # Fetch snippet
    snippet = Snippet.get_by_id(snippet_id)
    
    if not snippet:
        error(f"Snippet #{snippet_id} not found")
        console.print("\n[dim]Tip: Use 'qnote snippet list' to see all snippets[/dim]")
        return
    
    console.print(f"[cyan]Editing snippet #{snippet_id}...[/cyan]")
    if snippet.title:
        console.print(f"[dim]Title: {snippet.title}[/dim]")
    if snippet.language:
        console.print(f"[dim]Language: {snippet.language}[/dim]")
    
    # Determine file extension
    extension = f".{snippet.language}" if snippet.language else ".txt"
    
    # Open in editor
    try:
        edited_code = open_in_editor(
            initial_content=snippet.code,
            extension=extension
        )
        
        if not edited_code:
            warning("No changes made - code is empty or unchanged")
            return
        
        # Check if actually changed
        if edited_code == snippet.code:
            console.print("[yellow]No changes made[/yellow]")
            return
        
        # Update snippet
        snippet.code = edited_code
        snippet.save()
        
        success(f"Snippet #{snippet_id} updated successfully!")
        
        # Show stats
        lines = len(edited_code.splitlines())
        console.print(f"[dim]Lines: {lines}[/dim]\n")
        
    except EditorError as e:
        error(f"Editor error: {e}")
    except Exception as e:
        error(f"Failed to update snippet: {e}")


def edit_todo(todo_id: int) -> None:
    """
    Edit a TODO's description in external editor.
    
    Args:
        todo_id: TODO ID to edit
    """
    # Fetch TODO
    todo = Todo.get_by_id(todo_id)
    
    if not todo:
        error(f"TODO #{todo_id} not found")
        console.print("\n[dim]Tip: Use 'qnote todo list' to see all TODOs[/dim]")
        return
    
    console.print(f"[cyan]Editing TODO #{todo_id} description...[/cyan]")
    console.print(f"[dim]Title: {todo.title}[/dim]")
    
    # Open in editor
    try:
        edited_description = open_in_editor(
            initial_content=todo.description or "",
            extension=".txt"
        )
        
        if edited_description is None:
            warning("No changes made")
            return
        
        # Check if actually changed
        if edited_description == (todo.description or ""):
            console.print("[yellow]No changes made[/yellow]")
            return
        
        # Update TODO
        todo.description = edited_description if edited_description.strip() else None
        todo.save()
        
        success(f"TODO #{todo_id} updated successfully!")
        
        if todo.description:
            preview = todo.description[:80] + "..." if len(todo.description) > 80 else todo.description
            console.print(f"\n[dim]Description: {preview}[/dim]\n")
        
    except EditorError as e:
        error(f"Editor error: {e}")
    except Exception as e:
        error(f"Failed to update TODO: {e}")
