#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qnote.commands.delete - Delete Command Implementations

Delete items with confirmation.

Copyright (c) 2026 qnote
Licensed under the MIT License.
"""

from typing import Tuple
from rich.console import Console
from rich.prompt import Confirm

from qnote.core.note import Note
from qnote.core.snippet import Snippet
from qnote.core.todo import Todo
from qnote.utils.formatter import success, error, warning

console = Console()


def delete_notes(note_ids: Tuple[int, ...], force: bool = False) -> None:
    """
    Delete one or more notes.
    
    Args:
        note_ids: Tuple of note IDs to delete
        force: If True, skip confirmation
    
    Examples:
        >>> delete_notes((1,))
        >>> delete_notes((1, 2, 3), force=True)
    """
    if not note_ids:
        error("No note IDs provided")
        return
    
    # Fetch notes to verify they exist
    notes = []
    not_found = []
    
    for note_id in note_ids:
        note = Note.get_by_id(note_id)
        if note:
            notes.append(note)
        else:
            not_found.append(note_id)
    
    # Report not found
    if not_found:
        for nid in not_found:
            error(f"Note #{nid} not found")
    
    if not notes:
        return
    
    # Show what will be deleted
    console.print("\n[yellow]Notes to delete:[/yellow]")
    for note in notes:
        title = note.title or note.content[:50] + "..."
        console.print(f"  [cyan]#{note.id}[/cyan]: {title}")
    console.print()
    
    # Confirm deletion
    if not force:
        if len(notes) == 1:
            confirmed = Confirm.ask(f"Delete note #{notes[0].id}?", default=False)
        else:
            confirmed = Confirm.ask(f"Delete {len(notes)} notes?", default=False)
        
        if not confirmed:
            console.print("[yellow]Canceled[/yellow]")
            return
    
    # Delete notes
    deleted_count = 0
    for note in notes:
        try:
            note.delete()
            deleted_count += 1
        except Exception as e:
            error(f"Failed to delete note #{note.id}: {e}")
    
    # Report results
    if deleted_count > 0:
        success(f"Deleted {deleted_count} note{'s' if deleted_count > 1 else ''}")
    
    if deleted_count < len(notes):
        warning(f"Failed to delete {len(notes) - deleted_count} note(s)")


def delete_snippets(snippet_ids: Tuple[int, ...], force: bool = False) -> None:
    """
    Delete one or more code snippets.
    
    Args:
        snippet_ids: Tuple of snippet IDs to delete
        force: If True, skip confirmation
    """
    if not snippet_ids:
        error("No snippet IDs provided")
        return
    
    # Fetch snippets
    snippets = []
    not_found = []
    
    for snippet_id in snippet_ids:
        snippet = Snippet.get_by_id(snippet_id)
        if snippet:
            snippets.append(snippet)
        else:
            not_found.append(snippet_id)
    
    if not_found:
        for sid in not_found:
            error(f"Snippet #{sid} not found")
    
    if not snippets:
        return
    
    # Show what will be deleted
    console.print("\n[yellow]Snippets to delete:[/yellow]")
    for snippet in snippets:
        title = snippet.title or f"{snippet.language or 'code'} snippet"
        console.print(f"  [cyan]#{snippet.id}[/cyan]: {title}")
    console.print()
    
    # Confirm deletion
    if not force:
        if len(snippets) == 1:
            confirmed = Confirm.ask(f"Delete snippet #{snippets[0].id}?", default=False)
        else:
            confirmed = Confirm.ask(f"Delete {len(snippets)} snippets?", default=False)
        
        if not confirmed:
            console.print("[yellow]Canceled[/yellow]")
            return
    
    # Delete snippets
    deleted_count = 0
    for snippet in snippets:
        try:
            snippet.delete()
            deleted_count += 1
        except Exception as e:
            error(f"Failed to delete snippet #{snippet.id}: {e}")
    
    if deleted_count > 0:
        success(f"Deleted {deleted_count} snippet{'s' if deleted_count > 1 else ''}")
    
    if deleted_count < len(snippets):
        warning(f"Failed to delete {len(snippets) - deleted_count} snippet(s)")


def delete_todos(todo_ids: Tuple[int, ...], force: bool = False) -> None:
    """
    Delete one or more TODOs.
    
    Args:
        todo_ids: Tuple of TODO IDs to delete
        force: If True, skip confirmation
    """
    if not todo_ids:
        error("No TODO IDs provided")
        return
    
    # Fetch TODOs
    todos = []
    not_found = []
    
    for todo_id in todo_ids:
        todo = Todo.get_by_id(todo_id)
        if todo:
            todos.append(todo)
        else:
            not_found.append(todo_id)
    
    if not_found:
        for tid in not_found:
            error(f"TODO #{tid} not found")
    
    if not todos:
        return
    
    # Show what will be deleted
    console.print("\n[yellow]TODOs to delete:[/yellow]")
    for todo in todos:
        status = "✓" if todo.completed else "☐"
        console.print(f"  {status} [cyan]#{todo.id}[/cyan]: {todo.title}")
    console.print()
    
    # Confirm deletion
    if not force:
        if len(todos) == 1:
            confirmed = Confirm.ask(f"Delete TODO #{todos[0].id}?", default=False)
        else:
            confirmed = Confirm.ask(f"Delete {len(todos)} TODOs?", default=False)
        
        if not confirmed:
            console.print("[yellow]Canceled[/yellow]")
            return
    
    # Delete TODOs
    deleted_count = 0
    for todo in todos:
        try:
            todo.delete()
            deleted_count += 1
        except Exception as e:
            error(f"Failed to delete TODO #{todo.id}: {e}")
    
    if deleted_count > 0:
        success(f"Deleted {deleted_count} TODO{'s' if deleted_count > 1 else ''}")
    
    if deleted_count < len(todos):
        warning(f"Failed to delete {len(todos) - deleted_count} TODO(s)")
