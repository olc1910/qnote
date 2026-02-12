#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qnote.core.snippet - Code Snippet Model

This module defines the Snippet class for managing code snippets.
Snippets are pieces of code with syntax highlighting support,
language detection, and tag organization.

Features:
- CRUD operations for code snippets
- Language detection and syntax highlighting
- Tag management
- Search functionality
- Clipboard integration (copy code)

Copyright (c) 2026 Otis L. Crossley
Licensed under the MIT License.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from qnote.core.database import get_database


@dataclass
class Snippet:
    """
    Represents a code snippet in qnote.
    
    Attributes:
        id: Unique identifier (auto-generated)
        title: Optional snippet title
        code: The actual code content
        language: Programming language (python, javascript, etc.)
        description: Optional description
        tags: List of tag names
        created_at: Creation timestamp
        updated_at: Last update timestamp
        is_starred: Whether snippet is marked as favorite
    """
    
    code: str
    language: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_starred: bool = False
    
    def save(self) -> "Snippet":
        """
        Save snippet to database.
        
        Creates a new snippet if id is None, otherwise updates existing.
        
        Returns:
            Self for method chaining
        
        Raises:
            ValueError: If code is empty
        """
        if not self.code.strip():
            raise ValueError("Snippet code cannot be empty")
        
        db = get_database()
        
        with db.transaction() as conn:
            cursor = conn.cursor()
            
            if self.id is None:
                # Create new snippet
                cursor.execute(
                    """
                    INSERT INTO snippets (title, code, language, description, is_starred)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (self.title, self.code, self.language, self.description, self.is_starred)
                )
                self.id = cursor.lastrowid
                
                # Fetch timestamps
                cursor.execute(
                    "SELECT created_at, updated_at FROM snippets WHERE id = ?",
                    (self.id,)
                )
                row = cursor.fetchone()
                self.created_at = datetime.fromisoformat(row[0])
                self.updated_at = datetime.fromisoformat(row[1])
            else:
                # Update existing snippet
                cursor.execute(
                    """
                    UPDATE snippets
                    SET title = ?, code = ?, language = ?, description = ?, 
                        is_starred = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (self.title, self.code, self.language, self.description, 
                     self.is_starred, self.id)
                )
                
                # Fetch updated timestamp
                cursor.execute(
                    "SELECT updated_at FROM snippets WHERE id = ?",
                    (self.id,)
                )
                row = cursor.fetchone()
                self.updated_at = datetime.fromisoformat(row[0])
            
            # Handle tags
            self._save_tags(cursor)
        
        return self
    
    def _save_tags(self, cursor) -> None:
        """Save tags for this snippet."""
        if self.id is None:
            return
        
        # Remove existing tags
        cursor.execute("DELETE FROM snippet_tags WHERE snippet_id = ?", (self.id,))
        
        # Add new tags
        for tag_name in self.tags:
            tag_name = tag_name.strip().lower()
            if not tag_name:
                continue
            
            # Get or create tag
            cursor.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (tag_name,))
            cursor.execute("SELECT id FROM tags WHERE name = ?", (tag_name,))
            tag_id = cursor.fetchone()[0]
            
            # Link snippet to tag
            cursor.execute(
                "INSERT INTO snippet_tags (snippet_id, tag_id) VALUES (?, ?)",
                (self.id, tag_id)
            )
    
    def delete(self) -> None:
        """Delete snippet from database."""
        if self.id is None:
            raise ValueError("Cannot delete unsaved snippet")
        
        db = get_database()
        with db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM snippets WHERE id = ?", (self.id,))
    
    @staticmethod
    def get_by_id(snippet_id: int) -> Optional["Snippet"]:
        """
        Retrieve snippet by ID.
        
        Args:
            snippet_id: Snippet ID to retrieve
        
        Returns:
            Snippet object or None if not found
        """
        db = get_database()
        conn = db.connect()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT id, title, code, language, description, created_at, updated_at, is_starred
            FROM snippets WHERE id = ?
            """,
            (snippet_id,)
        )
        
        row = cursor.fetchone()
        if not row:
            return None
        
        # Get tags
        cursor.execute(
            """
            SELECT t.name FROM tags t
            JOIN snippet_tags st ON t.id = st.tag_id
            WHERE st.snippet_id = ?
            """,
            (snippet_id,)
        )
        tags = [row[0] for row in cursor.fetchall()]
        
        return Snippet(
            id=row[0],
            title=row[1],
            code=row[2],
            language=row[3],
            description=row[4],
            created_at=datetime.fromisoformat(row[5]),
            updated_at=datetime.fromisoformat(row[6]),
            is_starred=bool(row[7]),
            tags=tags
        )
    
    @staticmethod
    def get_all(
        limit: Optional[int] = None,
        offset: int = 0,
        language: Optional[str] = None,
        tags: Optional[List[str]] = None,
        starred_only: bool = False
    ) -> List["Snippet"]:
        """
        Get all snippets with optional filtering.
        
        Args:
            limit: Maximum number of snippets to return
            offset: Number of snippets to skip
            language: Filter by programming language
            tags: Filter by tags
            starred_only: If True, return only starred snippets
        
        Returns:
            List of Snippet objects
        """
        db = get_database()
        conn = db.connect()
        cursor = conn.cursor()
        
        # Build query
        query = "SELECT DISTINCT s.id FROM snippets s"
        conditions = []
        params = []
        
        if tags:
            query += """
                JOIN snippet_tags st ON s.id = st.snippet_id
                JOIN tags t ON st.tag_id = t.id
            """
            placeholders = ",".join("?" * len(tags))
            conditions.append(f"t.name IN ({placeholders})")
            params.extend(tags)
        
        if language:
            conditions.append("s.language = ?")
            params.append(language)
        
        if starred_only:
            conditions.append("s.is_starred = 1")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY s.updated_at DESC"
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        if offset:
            query += " OFFSET ?"
            params.append(offset)
        
        cursor.execute(query, params)
        snippet_ids = [row[0] for row in cursor.fetchall()]
        
        return [Snippet.get_by_id(sid) for sid in snippet_ids if Snippet.get_by_id(sid)]
    
    @staticmethod
    def detect_language(code: str, filename: Optional[str] = None) -> Optional[str]:
        """
        Detect programming language from code or filename.
        
        Args:
            code: Code content
            filename: Optional filename for extension-based detection
        
        Returns:
            Detected language or None
        
        TODO: Implement proper language detection using pygments or other library
        """
        # Simple extension-based detection for now
        if filename:
            ext_map = {
                ".py": "python",
                ".js": "javascript",
                ".ts": "typescript",
                ".java": "java",
                ".cpp": "cpp",
                ".c": "c",
                ".go": "go",
                ".rs": "rust",
                ".rb": "ruby",
                ".php": "php",
                ".sh": "bash",
                ".sql": "sql",
                ".html": "html",
                ".css": "css",
            }
            for ext, lang in ext_map.items():
                if filename.endswith(ext):
                    return lang
        
        # TODO: Implement content-based detection
        return None
    
    def __str__(self) -> str:
        """String representation of snippet."""
        title = self.title or f"{self.language or 'code'} snippet"
        return f"Snippet #{self.id}: {title}"
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Snippet(id={self.id}, language='{self.language}', tags={self.tags})"
