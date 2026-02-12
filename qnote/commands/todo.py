#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qnote.commands.todo - TODO Command Implementations

Additional TODO management commands.

Copyright (c) 2026 qnote
Licensed under the MIT License.
"""

from rich.console import Console

from qnote.core.todo import Todo
from qnote.utils.formatter import success, error

console = Console()


def mark_todo_done(todo_id: int) -> None:
    """
    Mark a TODO as completed.
    
    Args:
        todo_id: TODO ID to mark as done
    
    Examples:
        >>> mark_todo_done(42)
    """
    # Fetch TODO
    todo = Todo.get_by_id(todo_id)
    
    if not todo:
        error(f"TODO #{todo_id} not found")
        console.print("\n[dim]Tip: Use 'qnote todo list' to see all TODOs[/dim]")
        return
    
    if todo.completed:
        console.print(f"[yellow]TODO #{todo_id} is already completed[/yellow]")
        return
    
    # Mark as done
    try:
        todo.complete()
        success(f"✓ TODO #{todo_id} marked as completed!")
        console.print(f"[dim]  {todo.title}[/dim]\n")
    except Exception as e:
        error(f"Failed to update TODO: {e}")


def mark_todo_undone(todo_id: int) -> None:
    """
    Mark a TODO as not completed (pending).
    
    Args:
        todo_id: TODO ID to mark as pending
    
    Examples:
        >>> mark_todo_undone(42)
    """
    # Fetch TODO
    todo = Todo.get_by_id(todo_id)
    
    if not todo:
        error(f"TODO #{todo_id} not found")
        console.print("\n[dim]Tip: Use 'qnote todo list' to see all TODOs[/dim]")
        return
    
    if not todo.completed:
        console.print(f"[yellow]TODO #{todo_id} is already pending[/yellow]")
        return
    
    # Mark as not done
    try:
        todo.uncomplete()
        success(f"☐ TODO #{todo_id} marked as pending")
        console.print(f"[dim]  {todo.title}[/dim]\n")
    except Exception as e:
        error(f"Failed to update TODO: {e}")
