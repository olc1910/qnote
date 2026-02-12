#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qnote.utils.editor - External Editor Integration

This module handles opening external editors (vim, nano, vscode, etc.)
for editing note content. It creates temporary files, opens the editor,
and reads back the content after editing.

Supports:
- $EDITOR environment variable
- Custom editor from config
- Fallback to vim/nano
- Proper cleanup of temporary files

Copyright (c) 2026 Otis L. Crossley
Licensed under the MIT License.
"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from qnote.utils.config import get_config


class EditorError(Exception):
    """Raised when editor operation fails."""
    pass


def open_in_editor(
    initial_content: str = "",
    extension: str = ".md",
    editor: Optional[str] = None
) -> Optional[str]:
    """
    Open content in external editor and return edited content.
    
    Creates a temporary file with the initial content, opens it in
    the configured editor, and returns the edited content.
    
    Args:
        initial_content: Initial text to populate the editor
        extension: File extension for the temp file (affects syntax highlighting)
        editor: Editor command to use (if None, uses config or $EDITOR)
    
    Returns:
        Edited content or None if user canceled (file empty or unchanged)
    
    Raises:
        EditorError: If editor fails to open or execute
    
    Examples:
        content = open_in_editor("Initial note", ".md")
        code = open_in_editor("# Python code", ".py", "code --wait")
    """
    # Determine which editor to use
    if editor is None:
        config = get_config()
        editor = config.get("editor")
    
    if not editor:
        raise EditorError("No editor configured. Set $EDITOR or configure via 'qnote config set editor <cmd>'")
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix=extension,
        delete=False,
        encoding='utf-8'
    ) as tmp_file:
        tmp_path = Path(tmp_file.name)
        tmp_file.write(initial_content)
    
    try:
        # Open editor
        # Split editor command to handle arguments (e.g., "code --wait")
        editor_parts = editor.split()
        subprocess.run(
            editor_parts + [str(tmp_path)],
            check=True
        )
        
        # Read edited content
        with open(tmp_path, 'r', encoding='utf-8') as f:
            edited_content = f.read()
        
        # Return None if content is empty or unchanged
        if not edited_content.strip():
            return None
        
        if edited_content == initial_content:
            return None
        
        return edited_content
    
    except subprocess.CalledProcessError as e:
        raise EditorError(f"Editor exited with error code {e.returncode}")
    except FileNotFoundError:
        raise EditorError(f"Editor '{editor}' not found. Please check your configuration.")
    except Exception as e:
        raise EditorError(f"Failed to open editor: {e}")
    finally:
        # Clean up temporary file
        try:
            tmp_path.unlink()
        except Exception:
            pass  # Ignore cleanup errors


def get_editor_command() -> str:
    """
    Get the configured editor command.
    
    Returns:
        Editor command string
    
    Examples:
        >>> get_editor_command()
        'vim'
    """
    config = get_config()
    return config.get("editor", "vim")


def set_editor_command(editor: str) -> None:
    """
    Set the editor command in configuration.
    
    Args:
        editor: Editor command to use
    
    Examples:
        set_editor_command('nvim')
        set_editor_command('code --wait')
    """
    config = get_config()
    config.set("editor", editor)


def test_editor(editor: Optional[str] = None) -> bool:
    """
    Test if editor is available and working.
    
    Args:
        editor: Editor to test (if None, uses configured editor)
    
    Returns:
        True if editor is available and working
    
    Examples:
        >>> test_editor('vim')
        True
        >>> test_editor('nonexistent')
        False
    """
    if editor is None:
        editor = get_editor_command()
    
    try:
        # Try to get version or help (usually exits quickly)
        editor_parts = editor.split()[0]  # Just the command, not args
        subprocess.run(
            [editor_parts, "--version"],
            capture_output=True,
            timeout=5
        )
        return True
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        return False
