#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qnote.core.database - Database Management

This module handles all database operations for qnote.
It uses SQLite as the backend database and provides:
- Database initialization and schema creation
- Connection management
- Migration support
- Transaction handling

Database Schema:
- notes: Stores note content and metadata
- snippets: Stores code snippets
- todos: Stores TODO items
- tags: Stores unique tags
- note_tags: Many-to-many relationship between notes and tags

Copyright (c) 2026 Otis L. Crossley
Licensed under the MIT License.
"""

import sqlite3
from pathlib import Path
from typing import Optional
from contextlib import contextmanager


class Database:
    """
    Database manager for qnote.
    
    Handles SQLite database connection, schema creation, and migrations.
    Uses a singleton pattern to ensure only one database connection exists.
    
    Attributes:
        db_path: Path to the SQLite database file
        connection: SQLite connection object
    """
    
    # Current database schema version
    SCHEMA_VERSION = 1
    
    def __init__(self, db_path: Optional[Path] = None) -> None:
        """
        Initialize database connection.
        
        Args:
            db_path: Path to database file. If None, uses default location
                    (~/.local/share/qnote/qnote.db)
        """
        if db_path is None:
            # Default database location
            db_path = Path.home() / ".local" / "share" / "qnote" / "qnote.db"
        
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection: Optional[sqlite3.Connection] = None
        
        # Initialize database if it doesn't exist
        if not self.db_path.exists():
            self._initialize_database()
    
    def connect(self) -> sqlite3.Connection:
        """
        Get or create database connection.
        
        Returns:
            SQLite connection object
        """
        if self.connection is None:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row  # Access columns by name
        return self.connection
    
    def close(self) -> None:
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    @contextmanager
    def transaction(self):
        """
        Context manager for database transactions.
        
        Usage:
            with db.transaction():
                # Execute queries
                # Automatically commits on success, rolls back on error
        """
        conn = self.connect()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
    
    def _initialize_database(self) -> None:
        """
        Create database schema.
        
        Creates all necessary tables and indexes for qnote.
        This is called only once when the database is first created.
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        # Notes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_starred BOOLEAN DEFAULT 0
            )
        """)
        
        # Snippets table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS snippets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                code TEXT NOT NULL,
                language TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_starred BOOLEAN DEFAULT 0
            )
        """)
        
        # TODOs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed BOOLEAN DEFAULT 0,
                priority TEXT DEFAULT 'medium',
                due_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tags table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """)
        
        # Note-Tags relationship (many-to-many)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS note_tags (
                note_id INTEGER,
                tag_id INTEGER,
                FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
                PRIMARY KEY (note_id, tag_id)
            )
        """)
        
        # Snippet-Tags relationship
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS snippet_tags (
                snippet_id INTEGER,
                tag_id INTEGER,
                FOREIGN KEY (snippet_id) REFERENCES snippets(id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
                PRIMARY KEY (snippet_id, tag_id)
            )
        """)
        
        # TODO-Tags relationship
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todo_tags (
                todo_id INTEGER,
                tag_id INTEGER,
                FOREIGN KEY (todo_id) REFERENCES todos(id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
                PRIMARY KEY (todo_id, tag_id)
            )
        """)
        
        # Metadata table for versioning
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        
        # Store schema version
        cursor.execute(
            "INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)",
            ("schema_version", str(self.SCHEMA_VERSION))
        )
        
        # Create indexes for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_notes_created ON notes(created_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_notes_updated ON notes(updated_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_snippets_language ON snippets(language)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_todos_completed ON todos(completed)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_todos_priority ON todos(priority)")
        
        conn.commit()
    
    def get_schema_version(self) -> int:
        """
        Get current database schema version.
        
        Returns:
            Schema version number
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM metadata WHERE key = 'schema_version'")
        result = cursor.fetchone()
        return int(result[0]) if result else 0
    
    def migrate(self, target_version: Optional[int] = None) -> None:
        """
        Migrate database to target version.
        
        Args:
            target_version: Target schema version. If None, migrates to latest.
        
        TODO: Implement actual migration logic when schema changes
        """
        current_version = self.get_schema_version()
        target = target_version or self.SCHEMA_VERSION
        
        if current_version >= target:
            return
        
        # TODO: Implement migration steps
        # For now, this is a placeholder
        pass


# Singleton instance
_db_instance: Optional[Database] = None


def get_database(db_path: Optional[Path] = None) -> Database:
    """
    Get database singleton instance.
    
    Args:
        db_path: Path to database file (only used on first call)
    
    Returns:
        Database instance
    """
    global _db_instance
    if _db_instance is None:
        _db_instance = Database(db_path)
    return _db_instance
