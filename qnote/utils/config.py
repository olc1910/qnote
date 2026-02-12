#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qnote.utils.config - Configuration Management

This module handles loading, saving, and accessing qnote configuration.
Configuration is stored in YAML format at ~/.config/qnote/config.yaml

Configuration options:
- editor: External editor command (default: $EDITOR or vim)
- sync.remote: Git remote URL for sync
- sync.auto: Enable automatic sync after changes
- theme: Color theme (dark, light, auto)
- pager: Pager command for long outputs

Copyright (c) 2026 Otis L. Crossley
Licensed under the MIT License.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional
import yaml


class Config:
    """
    Configuration manager for qnote.
    
    Handles loading and saving configuration from YAML file.
    Provides get/set methods with dot notation for nested values.
    """
    
    DEFAULT_CONFIG = {
        "editor": os.environ.get("EDITOR", "vim"),
        "theme": "auto",
        "pager": "less",
        "sync": {
            "remote": None,
            "auto": False,
        },
        "database": {
            "path": str(Path.home() / ".local" / "share" / "qnote" / "qnote.db"),
        },
    }
    
    def __init__(self, config_path: Optional[Path] = None) -> None:
        """
        Initialize configuration.
        
        Args:
            config_path: Path to config file. If None, uses default location.
        """
        if config_path is None:
            config_path = Path.home() / ".config" / "qnote" / "config.yaml"
        
        self.config_path = config_path
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self._config: Dict[str, Any] = {}
        
        self.load()
    
    def load(self) -> None:
        """
        Load configuration from file.
        
        If file doesn't exist, creates it with default values.
        """
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                loaded_config = yaml.safe_load(f) or {}
                # Merge with defaults to ensure all keys exist
                self._config = self._merge_configs(self.DEFAULT_CONFIG.copy(), loaded_config)
        else:
            self._config = self.DEFAULT_CONFIG.copy()
            self.save()
    
    def save(self) -> None:
        """Save configuration to file."""
        with open(self.config_path, "w") as f:
            yaml.dump(self._config, f, default_flow_style=False)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'sync.remote')
            default: Default value if key doesn't exist
        
        Returns:
            Configuration value
        
        Examples:
            config.get('editor')  # Returns editor command
            config.get('sync.remote')  # Returns sync remote URL
        """
        keys = key.split(".")
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value using dot notation.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        
        Examples:
            config.set('editor', 'nvim')
            config.set('sync.remote', 'git@github.com:user/notes.git')
        """
        keys = key.split(".")
        current = self._config
        
        # Navigate to the correct nested level
        for k in keys[:-1]:
            if k not in current or not isinstance(current[k], dict):
                current[k] = {}
            current = current[k]
        
        # Set the value
        current[keys[-1]] = value
        self.save()
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get entire configuration as dictionary.
        
        Returns:
            Complete configuration dictionary
        """
        return self._config.copy()
    
    @staticmethod
    def _merge_configs(base: Dict, override: Dict) -> Dict:
        """
        Merge two configuration dictionaries recursively.
        
        Args:
            base: Base configuration
            override: Configuration to merge in
        
        Returns:
            Merged configuration
        """
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = Config._merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result


# Singleton instance
_config_instance: Optional[Config] = None


def get_config(config_path: Optional[Path] = None) -> Config:
    """
    Get configuration singleton instance.
    
    Args:
        config_path: Path to config file (only used on first call)
    
    Returns:
        Config instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_path)
    return _config_instance
