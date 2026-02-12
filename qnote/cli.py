#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qnote.cli - Main CLI Interface

This module provides the main command-line interface for qnote.
It uses Click to handle command routing and argument parsing.

The CLI is organized into command groups:
- Notes: add, list, show, edit, delete
- Snippets: snippet (with subcommands)
- TODOs: todo (with subcommands)
- Search: search
- Sync: sync (with subcommands)
- Config: config (with subcommands)

Copyright (c) 2026 Otis L. Crossley
Licensed under the MIT License.
"""

import click
from rich.console import Console

from qnote import __version__

# Initialize Rich console for beautiful terminal output
console = Console()


def _get_config_keys(ctx, args, incomplete):
    """
    Provide completion for config keys.
    Returns list of valid config keys with descriptions.
    """
    config_keys = {
        'editor': 'Text editor command (vim, nvim, nano, code, etc.)',
        'theme': 'Color theme (auto, dark, light)',
        'pager': 'Pager command (less, more, cat)',
        'database.path': 'SQLite database file path',
        'sync.remote': 'Git remote URL for sync',
        'sync.auto': 'Enable automatic sync (true/false)',
    }
    
    # Return keys that match the incomplete text
    return [(k, v) for k, v in config_keys.items() if k.startswith(incomplete)]


def _get_config_values(ctx, args, incomplete):
    """
    Provide completion for config values based on the key.
    """
    # Get the key from args
    if len(args) < 2:
        return []
    
    key = args[-1]
    
    # Predefined values for specific keys
    value_completions = {
        'editor': ['vim', 'nvim', 'nano', 'emacs', 'code', 'vi'],
        'theme': ['auto', 'dark', 'light'],
        'pager': ['less', 'more', 'cat'],
        'sync.auto': ['true', 'false'],
    }
    
    if key in value_completions:
        return [v for v in value_completions[key] if v.startswith(incomplete)]
    
    return []


def _get_languages(ctx, args, incomplete):
    """Provide common programming language completions."""
    languages = [
        'python', 'bash', 'javascript', 'typescript', 'java', 'c', 'cpp', 
        'rust', 'go', 'ruby', 'php', 'sql', 'html', 'css', 'json', 'yaml',
        'markdown', 'shell', 'powershell', 'perl', 'swift', 'kotlin'
    ]
    return [lang for lang in languages if lang.startswith(incomplete)]


@click.group()
@click.version_option(version=__version__, prog_name="qnote")
@click.option('--completion', type=click.Choice(['bash', 'zsh', 'fish']), 
              hidden=True, help='Generate shell completion script')
@click.pass_context
def main(ctx: click.Context, completion: str) -> None:
    """
    qnote - Quick Note & Snippet Manager
    
    A minimalistic CLI tool for managing notes, code snippets, and TODOs
    directly from your terminal.
    
    Examples:
        qnote add "My first note"
        qnote list
        qnote search "keyword"
        qnote snippet add "print('hello')" -l python
    """
    # Handle completion generation
    if completion:
        import os
        shell = completion
        prog_name = 'qnote'
        
        if shell == 'bash':
            script = f"eval \"$(_QNOTE_COMPLETE=bash_source {prog_name})\""
        elif shell == 'zsh':
            script = f"eval \"$(_QNOTE_COMPLETE=zsh_source {prog_name})\""
        elif shell == 'fish':
            script = f"eval \"(_QNOTE_COMPLETE=fish_source {prog_name})\""
        else:
            script = ""
        
        console.print(f"# Add this to your shell configuration file:")
        console.print(script)
        ctx.exit(0)
    
    # Ensure context object exists for passing data between commands
    ctx.ensure_object(dict)


@main.command()
@click.argument("content", required=False)
@click.option("-t", "--tags", help="Comma-separated tags")
@click.option("-e", "--editor", is_flag=True, help="Open in external editor")
@click.option("--title", help="Note title")
@click.option("--starred", is_flag=True, help="Mark as starred/favorite")
def add(content: str, tags: str, editor: bool, title: str, starred: bool) -> None:
    """
    Add a new note.
    
    If content is not provided or --editor flag is used,
    an external editor will be opened.
    
    Examples:
        qnote add "Quick note"
        qnote add -t python,webdev "Note with tags"
        qnote add --editor
    """
    from qnote.commands.add import add_note
    add_note(content, tags, title, editor, starred)


@main.command()
@click.option("-t", "--tags", help="Filter by tags (comma-separated)")
@click.option("--limit", type=int, default=50, help="Maximum number of results")
@click.option("--sort", type=click.Choice(["created", "updated", "title"]), 
              default="updated", help="Sort order")
@click.option("--starred", is_flag=True, help="Show only starred notes")
def list(tags: str, limit: int, sort: str, starred: bool) -> None:
    """
    List all notes.
    
    Examples:
        qnote list
        qnote list --tags python
        qnote list --limit 10 --sort created
    """
    from qnote.commands.list import list_notes
    list_notes(tags, limit, sort, starred)


@main.command()
@click.argument("note_id", type=int)
def show(note_id: int) -> None:
    """
    Show a specific note by ID.
    
    Examples:
        qnote show 42
    """
    from qnote.commands.show import show_note
    show_note(note_id)


@main.command()
@click.argument("note_id", type=int)
def edit(note_id: int) -> None:
    """
    Edit a note in external editor.
    
    Examples:
        qnote edit 42
    """
    from qnote.commands.edit import edit_note
    edit_note(note_id)


@main.command()
@click.argument("note_ids", nargs=-1, type=int, required=True)
@click.option("-f", "--force", is_flag=True, help="Skip confirmation")
def delete(note_ids: tuple, force: bool) -> None:
    """
    Delete one or more notes.
    
    Examples:
        qnote delete 42
        qnote delete 1 2 3 --force
    """
    from qnote.commands.delete import delete_notes
    delete_notes(note_ids, force)


@main.command()
@click.argument("query")
@click.option("--type", type=click.Choice(["note", "snippet", "todo", "all"]), 
              default="all", help="Type of items to search")
@click.option("-t", "--tags", help="Filter by tags")
@click.option("--limit", type=int, default=50, help="Maximum results")
def search(query: str, type: str, tags: str, limit: int) -> None:
    """
    Search through all notes, snippets, and TODOs.
    
    Examples:
        qnote search "python"
        qnote search "function" --type snippet
        qnote search "bug" --tags urgent
    """
    from qnote.commands.search import search_all
    search_all(query, type, tags, limit)


# Snippet command group
@main.group()
def snippet() -> None:
    """Manage code snippets."""
    pass


@snippet.command(name="add")
@click.argument("code", required=False)
@click.option("-l", "--language", help="Programming language", shell_complete=_get_languages)
@click.option("-t", "--tags", help="Comma-separated tags")
@click.option("--title", help="Snippet title")
@click.option("--from-file", type=click.Path(exists=True), help="Read from file")
@click.option("--starred", is_flag=True, help="Mark as starred")
def snippet_add(code: str, language: str, tags: str, title: str, from_file: str, starred: bool) -> None:
    """
    Add a code snippet.
    
    Examples:
        qnote snippet add "print('hello')" -l python
        qnote snippet add --from-file script.py
    """
    from qnote.commands.add import add_snippet
    add_snippet(code, language, title, None, tags, from_file, starred)


@snippet.command(name="list")
@click.option("-l", "--language", help="Filter by language", shell_complete=_get_languages)
@click.option("-t", "--tags", help="Filter by tags")
@click.option("--starred", is_flag=True, help="Show only starred snippets")
@click.option("--limit", type=int, default=50, help="Maximum number of results")
def snippet_list(language: str, tags: str, starred: bool, limit: int) -> None:
    """
    List all code snippets.
    
    Examples:
        qnote snippet list
        qnote snippet list --language python
        qnote snippet list --starred
    """
    from qnote.commands.list import list_snippets
    list_snippets(language, tags, limit, starred)


@snippet.command(name="show")
@click.argument("snippet_id", type=int)
def snippet_show(snippet_id: int) -> None:
    """
    Show a snippet by ID with syntax highlighting.
    
    Examples:
        qnote snippet show 42
    """
    from qnote.commands.show import show_snippet
    show_snippet(snippet_id)


@snippet.command(name="edit")
@click.argument("snippet_id", type=int)
def snippet_edit(snippet_id: int) -> None:
    """
    Edit a snippet in external editor.
    
    Examples:
        qnote snippet edit 42
    """
    from qnote.commands.edit import edit_snippet
    edit_snippet(snippet_id)


@snippet.command(name="delete")
@click.argument("snippet_ids", nargs=-1, type=int, required=True)
@click.option("-f", "--force", is_flag=True, help="Skip confirmation")
def snippet_delete(snippet_ids: tuple, force: bool) -> None:
    """
    Delete one or more snippets.
    
    Examples:
        qnote snippet delete 42
        qnote snippet delete 1 2 3 --force
    """
    from qnote.commands.delete import delete_snippets
    delete_snippets(snippet_ids, force)


# TODO command group
@main.group()
def todo() -> None:
    """Manage TODOs and tasks."""
    pass


@todo.command(name="add")
@click.argument("title")
@click.option("-p", "--priority", type=click.Choice(["low", "medium", "high"]), 
              default="medium", help="Priority level")
@click.option("-d", "--due", help="Due date (YYYY-MM-DD)")
@click.option("--description", help="Task description")
@click.option("-t", "--tags", help="Comma-separated tags")
def todo_add(title: str, priority: str, due: str, description: str, tags: str) -> None:
    """
    Add a new TODO.
    
    Examples:
        qnote todo add "Finish project"
        qnote todo add "Review code" -p high -d 2026-03-01
    """
    from qnote.commands.add import add_todo
    add_todo(title, description, priority, due, tags)


@todo.command(name="list")
@click.option("--pending", is_flag=True, help="Show only pending TODOs")
@click.option("--completed", is_flag=True, help="Show only completed TODOs")
@click.option("-p", "--priority", type=click.Choice(["low", "medium", "high"]), help="Filter by priority")
@click.option("-t", "--tags", help="Filter by tags")
@click.option("--overdue", is_flag=True, help="Show only overdue TODOs")
@click.option("--limit", type=int, default=50, help="Maximum number of results")
def todo_list(pending: bool, completed: bool, priority: str, tags: str, overdue: bool, limit: int) -> None:
    """
    List all TODO items.
    
    Examples:
        qnote todo list
        qnote todo list --pending
        qnote todo list --priority high
        qnote todo list --overdue
    """
    from qnote.commands.list import list_todos
    
    # Handle pending/completed flags
    completed_filter = None
    if pending and not completed:
        completed_filter = False
    elif completed and not pending:
        completed_filter = True
    
    list_todos(completed_filter, priority, tags, limit, overdue)


@todo.command(name="show")
@click.argument("todo_id", type=int)
def todo_show(todo_id: int) -> None:
    """
    Show a TODO by ID.
    
    Examples:
        qnote todo show 42
    """
    from qnote.commands.show import show_todo
    show_todo(todo_id)


@todo.command(name="done")
@click.argument("todo_id", type=int)
def todo_done(todo_id: int) -> None:
    """
    Mark a TODO as completed.
    
    Examples:
        qnote todo done 42
    """
    from qnote.commands.todo import mark_todo_done
    mark_todo_done(todo_id)


@todo.command(name="undone")
@click.argument("todo_id", type=int)
def todo_undone(todo_id: int) -> None:
    """
    Mark a TODO as not completed.
    
    Examples:
        qnote todo undone 42
    """
    from qnote.commands.todo import mark_todo_undone
    mark_todo_undone(todo_id)


@todo.command(name="edit")
@click.argument("todo_id", type=int)
def todo_edit(todo_id: int) -> None:
    """
    Edit a TODO's description.
    
    Examples:
        qnote todo edit 42
    """
    from qnote.commands.edit import edit_todo
    edit_todo(todo_id)


@todo.command(name="delete")
@click.argument("todo_ids", nargs=-1, type=int, required=True)
@click.option("-f", "--force", is_flag=True, help="Skip confirmation")
def todo_delete(todo_ids: tuple, force: bool) -> None:
    """
    Delete one or more TODOs.
    
    Examples:
        qnote todo delete 42
        qnote todo delete 1 2 3 --force
    """
    from qnote.commands.delete import delete_todos
    delete_todos(todo_ids, force)


# Sync command group
@main.group()
def sync() -> None:
    """Synchronize notes across devices."""
    pass


@sync.command(name="init")
@click.argument("remote_url")
def sync_init(remote_url: str) -> None:
    """
    Initialize sync with a remote repository.
    
    Examples:
        qnote sync init git@github.com:user/notes.git
    """
    console.print("[yellow]Note: sync init command not yet implemented[/yellow]")
    # TODO: Implement sync initialization


# Config command group
@main.group()
def config() -> None:
    """Manage qnote configuration."""
    pass


@config.command(name="list")
def config_list() -> None:
    """Show current configuration."""
    from qnote.commands.config import config_list as cmd_config_list
    cmd_config_list()


def _get_config_keys(ctx, args, incomplete):
    """
    Provide completion for config keys.
    Returns list of valid config keys with descriptions.
    """
    config_keys = {
        'editor': 'Text editor command (vim, nvim, nano, code, etc.)',
        'theme': 'Color theme (auto, dark, light)',
        'pager': 'Pager command (less, more, cat)',
        'database.path': 'SQLite database file path',
        'sync.remote': 'Git remote URL for sync',
        'sync.auto': 'Enable automatic sync (true/false)',
    }
    
    # Return keys that match the incomplete text
    return [(k, v) for k, v in config_keys.items() if k.startswith(incomplete)]


def _get_config_values(ctx, args, incomplete):
    """
    Provide completion for config values based on the key.
    """
    # Get the key from args
    if len(args) < 2:
        return []
    
    key = args[-1]
    
    # Predefined values for specific keys
    value_completions = {
        'editor': ['vim', 'nvim', 'nano', 'emacs', 'code', 'vi'],
        'theme': ['auto', 'dark', 'light'],
        'pager': ['less', 'more', 'cat'],
        'sync.auto': ['true', 'false'],
    }
    
    if key in value_completions:
        return [v for v in value_completions[key] if v.startswith(incomplete)]
    
    return []


@config.command(name="set")
@click.argument("key", shell_complete=_get_config_keys)
@click.argument("value", shell_complete=_get_config_values)
def config_set(key: str, value: str) -> None:
    """
    Set a configuration value.
    
    Examples:
        qnote config set editor nvim
        qnote config set theme dark
        qnote config set sync.auto true
    """
    from qnote.commands.config import config_set as cmd_config_set
    cmd_config_set(key, value)


@config.command(name="get")
@click.argument("key", shell_complete=_get_config_keys)
def config_get(key: str) -> None:
    """
    Get a configuration value.
    
    Examples:
        qnote config get editor
        qnote config get sync.remote
    """
    from qnote.commands.config import config_get as cmd_config_get
    cmd_config_get(key)


@config.command(name="reset")
@click.confirmation_option(prompt="Are you sure you want to reset all configuration to defaults?")
def config_reset() -> None:
    """Reset configuration to defaults."""
    from qnote.commands.config import config_reset as cmd_config_reset
    cmd_config_reset()


@config.command(name="path")
def config_path() -> None:
    """Show path to configuration file."""
    from qnote.commands.config import config_path as cmd_config_path
    cmd_config_path()


if __name__ == "__main__":
    main()
