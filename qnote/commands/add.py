#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qnote.commands.add - Add Command Implementations

This module implements all 'add' commands for creating new items:
- add_note: Create new notes
- add_snippet: Create code snippets
- add_todo: Create TODO items

Copyright (c) 2026 qnote
Licensed under the MIT License.
"""

from typing import Optional, List
from pathlib import Path
from datetime import datetime

from rich.console import Console

from qnote.core.note import Note
from qnote.core.snippet import Snippet
from qnote.core.todo import Todo
from qnote.utils.editor import open_in_editor, EditorError
from qnote.utils.formatter import success, error, warning

console = Console()


def add_note(
    content: Optional[str] = None,
    tags: Optional[str] = None,
    title: Optional[str] = None,
    use_editor: bool = False,
    starred: bool = False
) -> None:
    """
    Add a new note to the database.
    
    This function handles note creation with support for:
    - Direct content input via command line
    - External editor integration
    - Tag management
    - Optional title
    
    Args:
        content: Note content (optional if using editor)
        tags: Comma-separated tag string (e.g., "python,tutorial")
        title: Optional note title
        use_editor: If True, open external editor for content input
        starred: If True, mark note as starred/favorite
    
    Examples:
        >>> add_note("Quick note")
        >>> add_note("Python tips", tags="python,programming", title="Tips")
        >>> add_note(use_editor=True)
    
    Note:
        If use_editor is True or content is None, an external editor
        will be opened using the configured editor (see config.yaml).
    """
    # Case 1: Use external editor
    if use_editor or not content:
        try:
            edited_content = open_in_editor(
                initial_content=content or "",
                extension=".md"  # Markdown for syntax highlighting
            )
            
            # User canceled or provided no content
            if not edited_content:
                console.print("[yellow]✗ Canceled - no content provided[/yellow]")
                return
            
            content = edited_content
            
        except EditorError as e:
            error(f"Editor error: {e}")
            console.print("\n[dim]Tip: Configure editor with:[/dim]")
            console.print("[dim]  qnote config set editor vim[/dim]")
            console.print("[dim]  qnote config set editor 'code --wait'[/dim]")
            return
    
    # Case 2: Validate content
    if not content or not content.strip():
        error("Note content cannot be empty")
        console.print("\n[dim]Usage:[/dim]")
        console.print("[dim]  qnote add \"Your note content\"[/dim]")
        console.print("[dim]  qnote add --editor[/dim]")
        return
    
    # Parse tags from comma-separated string
    tag_list: List[str] = []
    if tags:
        tag_list = [
            tag.strip().lower() 
            for tag in tags.split(",") 
            if tag.strip()
        ]
        
        # Remove duplicates while preserving order
        seen = set()
        tag_list = [x for x in tag_list if not (x in seen or seen.add(x))]
    
    # Create and save note
    try:
        note = Note(
            content=content.strip(),
            title=title.strip() if title else None,
            tags=tag_list,
            is_starred=starred
        )
        note.save()
        
        # Success message
        star_icon = "★" if starred else ""
        success(f"Note #{note.id} created successfully! {star_icon}")
        
        # Show additional info
        if title:
            console.print(f"  [cyan]Title:[/cyan] {title}")
        if tag_list:
            console.print(f"  [cyan]Tags:[/cyan] {', '.join(tag_list)}")
        
        # Show preview
        preview = content[:100] + "..." if len(content) > 100 else content
        console.print(f"\n[dim]{preview}[/dim]\n")
        
    except ValueError as e:
        error(f"Failed to create note: {e}")
    except Exception as e:
        error(f"Unexpected error: {e}")
        console.print("\n[dim]Please report this issue on GitHub[/dim]")


def add_snippet(
    code: Optional[str] = None,
    language: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[str] = None,
    from_file: Optional[str] = None,
    starred: bool = False
) -> None:
    """
    Add a new code snippet to the database.
    
    Supports reading code from:
    - Direct command line input
    - File import
    - Pipe/stdin (future)
    
    Args:
        code: Snippet code content
        language: Programming language (python, javascript, etc.)
        title: Optional snippet title
        description: Optional description
        tags: Comma-separated tags
        from_file: Path to file to read code from
        starred: Mark as starred
    
    Examples:
        >>> add_snippet("print('hello')", language="python")
        >>> add_snippet(from_file="script.py", title="My Script")
        >>> add_snippet("console.log('hi')", language="javascript", 
        ...            tags="js,nodejs")
    
    Note:
        If language is not specified, the function attempts to
        detect it from the filename extension or code content.
    """
    # Read from file if specified
    if from_file:
        try:
            code_path = Path(from_file).expanduser()
            
            if not code_path.exists():
                error(f"File not found: {from_file}")
                console.print("\n[dim]Tip: Use absolute or relative path[/dim]")
                return
            
            if not code_path.is_file():
                error(f"Not a file: {from_file}")
                return
            
            # Read file content
            with open(code_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            console.print(f"[dim]→ Read {len(code)} characters from {code_path.name}[/dim]")
            
            # Auto-detect language from filename if not specified
            if not language:
                language = Snippet.detect_language(code, str(code_path))
                if language:
                    console.print(f"[dim]→ Detected language: {language}[/dim]")
            
            # Use filename as title if not specified
            if not title:
                title = code_path.stem  # Filename without extension
                
        except UnicodeDecodeError:
            error(f"Cannot read file: {from_file} (not a text file)")
            return
        except PermissionError:
            error(f"Permission denied: {from_file}")
            return
        except Exception as e:
            error(f"Failed to read file: {e}")
            return
    
    # Validate code
    if not code or not code.strip():
        error("Snippet code cannot be empty")
        console.print("\n[dim]Usage:[/dim]")
        console.print("[dim]  qnote snippet add \"code here\" -l python[/dim]")
        console.print("[dim]  qnote snippet add --from-file script.py[/dim]")
        return
    
    # Parse tags
    tag_list: List[str] = []
    if tags:
        tag_list = [
            tag.strip().lower() 
            for tag in tags.split(",") 
            if tag.strip()
        ]
    
    # Auto-add language as tag if not already present
    if language and language.lower() not in tag_list:
        tag_list.append(language.lower())
    
    # Create and save snippet
    try:
        snippet = Snippet(
            code=code.strip(),
            language=language,
            title=title.strip() if title else None,
            description=description,
            tags=tag_list,
            is_starred=starred
        )
        snippet.save()
        
        # Success message
        lang_display = language or "unknown"
        star_icon = "★" if starred else ""
        success(f"Snippet #{snippet.id} created successfully! ({lang_display}) {star_icon}")
        
        # Show additional info
        if title:
            console.print(f"  [cyan]Title:[/cyan] {title}")
        if description:
            desc_preview = description[:50] + "..." if len(description) > 50 else description
            console.print(f"  [cyan]Description:[/cyan] {desc_preview}")
        if tag_list:
            console.print(f"  [cyan]Tags:[/cyan] {', '.join(tag_list)}")
        
        console.print(f"  [cyan]Lines:[/cyan] {len(code.splitlines())}")
        
        # Show code preview
        lines = code.splitlines()
        preview_lines = lines[:3] if len(lines) > 3 else lines
        console.print("\n[dim]Preview:[/dim]")
        for line in preview_lines:
            console.print(f"[dim]  {line}[/dim]")
        if len(lines) > 3:
            console.print(f"[dim]  ... ({len(lines) - 3} more lines)[/dim]")
        console.print()
        
    except ValueError as e:
        error(f"Failed to create snippet: {e}")
    except Exception as e:
        error(f"Unexpected error: {e}")


def add_todo(
    title: str,
    description: Optional[str] = None,
    priority: str = "medium",
    due_date: Optional[str] = None,
    tags: Optional[str] = None
) -> None:
    """
    Add a new TODO item to the database.
    
    TODOs support:
    - Priority levels (low, medium, high)
    - Due dates
    - Tags for organization
    - Completion tracking
    
    Args:
        title: TODO title (required)
        description: Optional detailed description
        priority: Priority level - low, medium, or high (default: medium)
        due_date: Due date string in YYYY-MM-DD format
        tags: Comma-separated tags
    
    Examples:
        >>> add_todo("Finish project")
        >>> add_todo("Review code", priority="high", due_date="2026-03-01")
        >>> add_todo("Write docs", description="API documentation", 
        ...          tags="docs,important")
    
    Raises:
        ValueError: If priority is invalid or date format is wrong
    """
    # Validate priority
    valid_priorities = ["low", "medium", "high"]
    priority = priority.lower()
    
    if priority not in valid_priorities:
        error(f"Invalid priority: {priority}")
        console.print(f"\n[dim]Valid priorities: {', '.join(valid_priorities)}[/dim]")
        return
    
    # Parse and validate due date
    due_datetime = None
    if due_date:
        try:
            due_datetime = datetime.strptime(due_date, "%Y-%m-%d")
            
            # Warn if date is in the past
            if due_datetime.date() < datetime.now().date():
                warning(f"Due date is in the past: {due_date}")
                console.print("[dim]Continue anyway? The TODO will be created as overdue.[/dim]")
                
        except ValueError:
            error(f"Invalid date format: {due_date}")
            console.print("\n[dim]Expected format: YYYY-MM-DD[/dim]")
            console.print("[dim]Example: 2026-12-31[/dim]")
            return
    
    # Parse tags
    tag_list: List[str] = []
    if tags:
        tag_list = [
            tag.strip().lower() 
            for tag in tags.split(",") 
            if tag.strip()
        ]
    
    # Create and save TODO
    try:
        todo = Todo(
            title=title.strip(),
            description=description.strip() if description else None,
            priority=priority,
            due_date=due_datetime,
            tags=tag_list
        )
        todo.save()
        
        # Success message with priority indicator
        priority_colors = {
            "low": "green",
            "medium": "yellow",
            "high": "red"
        }
        priority_color = priority_colors[priority]
        
        success(f"TODO #{todo.id} created successfully!")
        console.print(f"  [cyan]Priority:[/cyan] [{priority_color}]{priority.upper()}[/{priority_color}]")
        
        # Show additional info
        if due_datetime:
            due_str = due_datetime.strftime('%Y-%m-%d')
            console.print(f"  [cyan]Due:[/cyan] {due_str}")
        
        if description:
            desc_preview = description[:60] + "..." if len(description) > 60 else description
            console.print(f"  [cyan]Description:[/cyan] {desc_preview}")
        
        if tag_list:
            console.print(f"  [cyan]Tags:[/cyan] {', '.join(tag_list)}")
        
        console.print()
        console.print("[dim]Tip: Mark as done with: qnote todo done <id>[/dim]")
        
    except ValueError as e:
        error(f"Failed to create TODO: {e}")
    except Exception as e:
        error(f"Unexpected error: {e}")
