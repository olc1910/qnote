#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qnote.commands.config - Configuration Management Commands

Handles displaying and modifying qnote configuration.

Copyright (c) 2026 Otis L. Crossley
Licensed under the MIT License.
"""

from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from rich.console import Console
from rich.table import Table

from qnote.utils.config import Config

console = Console()


def config_list() -> None:
    """
    Display current configuration.
    
    Shows all configuration values from the config file
    and indicates which values are overridden by environment variables.
    """
    try:
        config = Config()
        config_data = config.get_all()
        
        # Create table for display
        table = Table(title="qnote Configuration", show_header=True, header_style="bold cyan")
        table.add_column("Setting", style="green", width=20)
        table.add_column("Current Value", style="yellow", width=25)
        table.add_column("Available Values", style="dim cyan", width=35)
        table.add_column("Source", style="dim", width=10)
        
        # Define available values for each setting
        available_values = {
            'editor': 'vim, nvim, nano, emacs, code, etc.',
            'theme': 'auto, dark, light',
            'pager': 'less, more, cat, etc.',
            'database.path': 'any file path',
            'sync.remote': 'git URL or null',
            'sync.auto': 'true, false',
        }
        
        # Display configuration hierarchically
        def add_config_items(data: Dict[str, Any], prefix: str = "") -> None:
            """Recursively add config items to table"""
            for key, value in sorted(data.items()):
                full_key = f"{prefix}{key}" if prefix else key
                
                if isinstance(value, dict):
                    # Add separator for nested configs
                    table.add_row(f"[bold]{full_key}[/bold]", "", "", "")
                    add_config_items(value, f"{full_key}.")
                else:
                    # Check if value is from environment
                    env_var = f"QNOTE_{key.upper()}"
                    if key == "path" and prefix == "database.":
                        env_var = "QNOTE_DB"
                    elif key == "editor":
                        env_var = "EDITOR"
                    
                    import os
                    source = "env" if os.getenv(env_var) else "config"
                    
                    # Format value
                    if value is None:
                        value_str = "[dim]not set[/dim]"
                    elif isinstance(value, bool):
                        value_str = "true" if value else "false"
                    else:
                        value_str = str(value)
                    
                    # Get available values
                    avail = available_values.get(full_key, "")
                    
                    table.add_row(full_key, value_str, avail, source)
        
        add_config_items(config_data)
        console.print(table)
        
        # Show config file location
        console.print(f"\n[dim]Config file: {config.config_path}[/dim]")
        
        # Show usage hint
        console.print("\n[cyan]To set a value:[/cyan] qnote config set KEY VALUE")
        console.print("[dim]Example:[/dim] qnote config set editor nvim")
        console.print("[dim]Example:[/dim] qnote config set theme dark")
        
        # Show environment variable info
        import os
        env_overrides = []
        if os.getenv("EDITOR"):
            env_overrides.append("EDITOR")
        if os.getenv("QNOTE_DB"):
            env_overrides.append("QNOTE_DB")
        if os.getenv("QNOTE_CONFIG"):
            env_overrides.append("QNOTE_CONFIG")
        
        if env_overrides:
            console.print(f"\n[dim]Environment overrides: {', '.join(env_overrides)}[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error reading configuration: {e}[/red]")


def config_set(key: str, value: str) -> None:
    """
    Set a configuration value.
    
    Args:
        key: Configuration key (supports nested keys with dot notation, e.g., 'sync.remote')
        value: New value to set
    
    Examples:
        config_set('editor', 'nvim')
        config_set('theme', 'dark')
        config_set('sync.remote', 'git@github.com:user/notes.git')
    """
    try:
        config = Config()
        
        # Parse nested key (e.g., 'sync.remote' -> ['sync', 'remote'])
        keys = key.split('.')
        
        # Load current config
        config_data = config.get_all()
        
        # Navigate to the nested location
        current = config_data
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        # Convert value to appropriate type
        final_key = keys[-1]
        typed_value: Any = value
        
        # Try to parse as boolean
        if value.lower() in ('true', 'yes', '1'):
            typed_value = True
        elif value.lower() in ('false', 'no', '0'):
            typed_value = False
        elif value.lower() in ('null', 'none', ''):
            typed_value = None
        # Try to parse as number
        else:
            try:
                if '.' in value:
                    typed_value = float(value)
                else:
                    typed_value = int(value)
            except ValueError:
                typed_value = value  # Keep as string
        
        # Set the value
        current[final_key] = typed_value
        
        # Save config
        config.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config.config_path, 'w') as f:
            yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)
        
        console.print(f"[green]✓[/green] Set {key} = {typed_value}")
        
    except Exception as e:
        console.print(f"[red]Error setting configuration: {e}[/red]")


def config_get(key: str) -> None:
    """
    Get a specific configuration value.
    
    Args:
        key: Configuration key (supports nested keys with dot notation)
    
    Examples:
        config_get('editor')
        config_get('sync.remote')
    """
    try:
        config = Config()
        
        # Parse nested key
        keys = key.split('.')
        
        # Load current config
        config_data = config.get_all()
        
        # Navigate to the value
        current = config_data
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                console.print(f"[yellow]Configuration key '{key}' not found[/yellow]")
                return
        
        # Display the value
        if isinstance(current, dict):
            console.print(f"[cyan]{key}:[/cyan]")
            for k, v in current.items():
                console.print(f"  {k}: {v}")
        else:
            console.print(f"[cyan]{key}:[/cyan] {current}")
        
    except Exception as e:
        console.print(f"[red]Error getting configuration: {e}[/red]")


def config_reset() -> None:
    """
    Reset configuration to defaults.
    
    Backs up the current config file and creates a new one with default values.
    """
    try:
        config = Config()
        
        # Backup existing config
        if config.config_path.exists():
            backup_path = config.config_path.with_suffix('.yaml.backup')
            import shutil
            shutil.copy(config.config_path, backup_path)
            console.print(f"[dim]Backed up config to {backup_path}[/dim]")
        
        # Create default config
        default_config = {
            'editor': 'vim',
            'theme': 'auto',
            'pager': 'less',
            'sync': {
                'remote': None,
                'auto': False,
            },
            'database': {
                'path': str(Path.home() / '.local' / 'share' / 'qnote' / 'qnote.db'),
            },
        }
        
        # Write default config
        config.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config.config_path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False, sort_keys=False)
        
        console.print(f"[green]✓[/green] Configuration reset to defaults")
        console.print(f"[dim]Config file: {config.config_path}[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error resetting configuration: {e}[/red]")


def config_path() -> None:
    """
    Display the path to the configuration file.
    """
    try:
        config = Config()
        console.print(f"[cyan]Config file:[/cyan] {config.config_path}")
        
        if config.config_path.exists():
            console.print(f"[green]✓[/green] File exists")
        else:
            console.print(f"[yellow]![/yellow] File does not exist (will be created on first run)")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
