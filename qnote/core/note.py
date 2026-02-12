#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qnote.core.note - Note Model

This module defines the Note class and related operations.
A Note represents a text note with optional title, content,
tags, and metadata.

Features:
- Create, read, update, delete (CRUD) operations
- Tag management
- Markdown support
- Search functionality
- Starred/favorite notes

Copyright (c) 2026 Otis L. Crossley
Licensed under the MIT License.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from pathlib import Path

from qnote.core.database import get_database


@dataclass
class Note:
    """
    Represents a note in qnote.
    
    Attributes:
        id: Unique identifier (auto-generated)
        title: Optional note title
        content: Note content (supports Markdown)
        tags: List of tag names
        created_at: Creation timestamp
        updated_at: Last update timestamp
        is_starred: Whether note is marked as favorite
    """
    
    content: str
    title: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_starred: bool = False
    
    def save(self) -> "Note":
        """
        Save note to database.
        
        Creates a new note if id is None, otherwise updates existing note.
        
        Returns:
            Self for method chaining
        
        Raises:
            ValueError: If content is empty
        """
        if not self.content.strip():
            raise ValueError("Note content cannot be empty")
        
        db = get_database()
        
        with db.transaction() as conn:
            cursor = conn.cursor()
            
            if self.id is None:
                # Create new note
                cursor.execute(
                    """
                    INSERT INTO notes (title, content, is_starred)
                    VALUES (?, ?, ?)
                    """,
                    (self.title, self.content, self.is_starred)
                )
                self.id = cursor.lastrowid
                
                # Fetch timestamps
                cursor.execute(
                    "SELECT created_at, updated_at FROM notes WHERE id = ?",
                    (self.id,)
                )
                row = cursor.fetchone()
                self.created_at = datetime.fromisoformat(row[0])
                self.updated_at = datetime.fromisoformat(row[1])
            else:
                # Update existing note
                cursor.execute(
                    """
                    UPDATE notes
                    SET title = ?, content = ?, is_starred = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (self.title, self.content, self.is_starred, self.id)
                )
                
                # Fetch updated timestamp
                cursor.execute(
                    "SELECT updated_at FROM notes WHERE id = ?",
                    (self.id,)
                )
                row = cursor.fetchone()
                self.updated_at = datetime.fromisoformat(row[0])
            
            # Handle tags
            self._save_tags(cursor)
        
        return self
    
    def _save_tags(self, cursor) -> None:
        """
        Save tags for this note.
        
        Args:
            cursor: Database cursor
        """
        if self.id is None:
            return
        
        # Remove existing tags
        cursor.execute("DELETE FROM note_tags WHERE note_id = ?", (self.id,))
        
        # Add new tags
        for tag_name in self.tags:
            tag_name = tag_name.strip().lower()
            if not tag_name:
                continue
            
            # Get or create tag
            cursor.execute(
                "INSERT OR IGNORE INTO tags (name) VALUES (?)",
                (tag_name,)
            )
            cursor.execute("SELECT id FROM tags WHERE name = ?", (tag_name,))
            tag_id = cursor.fetchone()[0]
            
            # Link note to tag
            cursor.execute(
                "INSERT INTO note_tags (note_id, tag_id) VALUES (?, ?)",
                (self.id, tag_id)
            )
    
    def delete(self) -> None:
        """
        Delete note from database.
        
        Raises:
            ValueError: If note has no ID (not yet saved)
        """
        if self.id is None:
            raise ValueError("Cannot delete unsaved note")
        
        db = get_database()
        with db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM notes WHERE id = ?", (self.id,))
    
    @staticmethod
    def get_by_id(note_id: int) -> Optional["Note"]:
        """
        Retrieve note by ID.
        
        Args:
            note_id: Note ID to retrieve
        
        Returns:
            Note object or None if not found
        """
        db = get_database()
        conn = db.connect()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT id, title, content, created_at, updated_at, is_starred
            FROM notes WHERE id = ?
            """,
            (note_id,)
        )
        
        row = cursor.fetchone()
        if not row:
            return None
        
        # Get tags
        cursor.execute(
            """
            SELECT t.name FROM tags t
            JOIN note_tags nt ON t.id = nt.tag_id
            WHERE nt.note_id = ?
            """,
            (note_id,)
        )
        tags = [row[0] for row in cursor.fetchall()]
        
        return Note(
            id=row[0],
            title=row[1],
            content=row[2],
            created_at=datetime.fromisoformat(row[3]),
            updated_at=datetime.fromisoformat(row[4]),
            is_starred=bool(row[5]),
            tags=tags
        )
    
    @staticmethod
    def get_all(
        limit: Optional[int] = None,
        offset: int = 0,
        tags: Optional[List[str]] = None,
        starred_only: bool = False,
        sort_by: str = "updated_at"
    ) -> List["Note"]:
        """
        Get all notes with optional filtering.
        
        Args:
            limit: Maximum number of notes to return
            offset: Number of notes to skip
            tags: Filter by tags (returns notes with any of these tags)
            starred_only: If True, return only starred notes
            sort_by: Field to sort by (created_at, updated_at, title)
        
        Returns:
            List of Note objects
        """
        db = get_database()
        conn = db.connect()
        cursor = conn.cursor()
        
        # Build query
        query = "SELECT DISTINCT n.id FROM notes n"
        conditions = []
        params = []
        
        if tags:
            query += """
                JOIN note_tags nt ON n.id = nt.note_id
                JOIN tags t ON nt.tag_id = t.id
            """
            placeholders = ",".join("?" * len(tags))
            conditions.append(f"t.name IN ({placeholders})")
            params.extend(tags)
        
        if starred_only:
            conditions.append("n.is_starred = 1")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        # Add sorting
        sort_field = sort_by if sort_by in ["created_at", "updated_at", "title"] else "updated_at"
        query += f" ORDER BY n.{sort_field} DESC"
        
        # Add pagination
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        if offset:
            query += " OFFSET ?"
            params.append(offset)
        
        cursor.execute(query, params)
        note_ids = [row[0] for row in cursor.fetchall()]
        
        # Fetch full note objects
        return [Note.get_by_id(note_id) for note_id in note_ids if Note.get_by_id(note_id)]
    
    @staticmethod
    def search(query: str, tags: Optional[List[str]] = None) -> List["Note"]:
        """
        Search notes by content or title.
        
        Args:
            query: Search query string
            tags: Optional tag filter
        
        Returns:
            List of matching Note objects
        
        TODO: Implement full-text search with SQLite FTS5
        """
        db = get_database()
        conn = db.connect()
        cursor = conn.cursor()
        
        # Simple LIKE search for now
        # TODO: Upgrade to FTS5 for better performance
        search_query = """
            SELECT DISTINCT n.id FROM notes n
            WHERE n.content LIKE ? OR n.title LIKE ?
        """
        params = [f"%{query}%", f"%{query}%"]
        
        if tags:
            search_query += """
                AND n.id IN (
                    SELECT nt.note_id FROM note_tags nt
                    JOIN tags t ON nt.tag_id = t.id
                    WHERE t.name IN ({})
                )
            """.format(",".join("?" * len(tags)))
            params.extend(tags)
        
        cursor.execute(search_query, params)
        note_ids = [row[0] for row in cursor.fetchall()]
        
        return [Note.get_by_id(note_id) for note_id in note_ids if Note.get_by_id(note_id)]
    
    def __str__(self) -> str:
        """String representation of note."""
        title = self.title or "Untitled"
        return f"Note #{self.id}: {title}"
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Note(id={self.id}, title='{self.title}', tags={self.tags})"
