#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qnote.core.todo - TODO/Task Model

This module defines the Todo class for managing tasks and TODOs.
TODOs support priorities, due dates, completion status, and tags.

Features:
- CRUD operations for TODOs
- Priority levels (low, medium, high)
- Due date tracking
- Completion status
- Tag organization

Copyright (c) 2026 Otis L. Crossley
Licensed under the MIT License.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from qnote.core.database import get_database


@dataclass
class Todo:
    """
    Represents a TODO/task in qnote.
    
    Attributes:
        id: Unique identifier (auto-generated)
        title: Task title
        description: Optional detailed description
        completed: Completion status
        priority: Priority level (low, medium, high)
        due_date: Optional due date
        tags: List of tag names
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"
    due_date: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self) -> None:
        """Validate priority level."""
        valid_priorities = ["low", "medium", "high"]
        if self.priority not in valid_priorities:
            raise ValueError(f"Priority must be one of {valid_priorities}")
    
    def save(self) -> "Todo":
        """
        Save TODO to database.
        
        Creates a new TODO if id is None, otherwise updates existing.
        
        Returns:
            Self for method chaining
        
        Raises:
            ValueError: If title is empty
        """
        if not self.title.strip():
            raise ValueError("TODO title cannot be empty")
        
        db = get_database()
        
        with db.transaction() as conn:
            cursor = conn.cursor()
            
            due_date_str = self.due_date.isoformat() if self.due_date else None
            
            if self.id is None:
                # Create new TODO
                cursor.execute(
                    """
                    INSERT INTO todos (title, description, completed, priority, due_date)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (self.title, self.description, self.completed, self.priority, due_date_str)
                )
                self.id = cursor.lastrowid
                
                # Fetch timestamps
                cursor.execute(
                    "SELECT created_at, updated_at FROM todos WHERE id = ?",
                    (self.id,)
                )
                row = cursor.fetchone()
                self.created_at = datetime.fromisoformat(row[0])
                self.updated_at = datetime.fromisoformat(row[1])
            else:
                # Update existing TODO
                cursor.execute(
                    """
                    UPDATE todos
                    SET title = ?, description = ?, completed = ?, priority = ?, 
                        due_date = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (self.title, self.description, self.completed, 
                     self.priority, due_date_str, self.id)
                )
                
                # Fetch updated timestamp
                cursor.execute(
                    "SELECT updated_at FROM todos WHERE id = ?",
                    (self.id,)
                )
                row = cursor.fetchone()
                self.updated_at = datetime.fromisoformat(row[0])
            
            # Handle tags
            self._save_tags(cursor)
        
        return self
    
    def _save_tags(self, cursor) -> None:
        """Save tags for this TODO."""
        if self.id is None:
            return
        
        # Remove existing tags
        cursor.execute("DELETE FROM todo_tags WHERE todo_id = ?", (self.id,))
        
        # Add new tags
        for tag_name in self.tags:
            tag_name = tag_name.strip().lower()
            if not tag_name:
                continue
            
            # Get or create tag
            cursor.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (tag_name,))
            cursor.execute("SELECT id FROM tags WHERE name = ?", (tag_name,))
            tag_id = cursor.fetchone()[0]
            
            # Link TODO to tag
            cursor.execute(
                "INSERT INTO todo_tags (todo_id, tag_id) VALUES (?, ?)",
                (self.id, tag_id)
            )
    
    def complete(self) -> None:
        """Mark TODO as completed."""
        self.completed = True
        self.save()
    
    def uncomplete(self) -> None:
        """Mark TODO as not completed."""
        self.completed = False
        self.save()
    
    def delete(self) -> None:
        """Delete TODO from database."""
        if self.id is None:
            raise ValueError("Cannot delete unsaved TODO")
        
        db = get_database()
        with db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM todos WHERE id = ?", (self.id,))
    
    @property
    def is_overdue(self) -> bool:
        """Check if TODO is overdue."""
        if self.due_date is None or self.completed:
            return False
        return datetime.now() > self.due_date
    
    @staticmethod
    def get_by_id(todo_id: int) -> Optional["Todo"]:
        """
        Retrieve TODO by ID.
        
        Args:
            todo_id: TODO ID to retrieve
        
        Returns:
            Todo object or None if not found
        """
        db = get_database()
        conn = db.connect()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT id, title, description, completed, priority, due_date,
                   created_at, updated_at
            FROM todos WHERE id = ?
            """,
            (todo_id,)
        )
        
        row = cursor.fetchone()
        if not row:
            return None
        
        # Get tags
        cursor.execute(
            """
            SELECT t.name FROM tags t
            JOIN todo_tags tt ON t.id = tt.tag_id
            WHERE tt.todo_id = ?
            """,
            (todo_id,)
        )
        tags = [row[0] for row in cursor.fetchall()]
        
        # Parse due_date
        due_date = datetime.fromisoformat(row[5]) if row[5] else None
        
        return Todo(
            id=row[0],
            title=row[1],
            description=row[2],
            completed=bool(row[3]),
            priority=row[4],
            due_date=due_date,
            created_at=datetime.fromisoformat(row[6]),
            updated_at=datetime.fromisoformat(row[7]),
            tags=tags
        )
    
    @staticmethod
    def get_all(
        limit: Optional[int] = None,
        offset: int = 0,
        completed: Optional[bool] = None,
        priority: Optional[str] = None,
        tags: Optional[List[str]] = None,
        overdue_only: bool = False
    ) -> List["Todo"]:
        """
        Get all TODOs with optional filtering.
        
        Args:
            limit: Maximum number of TODOs to return
            offset: Number of TODOs to skip
            completed: Filter by completion status (None = all)
            priority: Filter by priority level
            tags: Filter by tags
            overdue_only: If True, return only overdue TODOs
        
        Returns:
            List of Todo objects
        """
        db = get_database()
        conn = db.connect()
        cursor = conn.cursor()
        
        # Build query
        query = "SELECT DISTINCT t.id FROM todos t"
        conditions = []
        params = []
        
        if tags:
            query += """
                JOIN todo_tags tt ON t.id = tt.todo_id
                JOIN tags tg ON tt.tag_id = tg.id
            """
            placeholders = ",".join("?" * len(tags))
            conditions.append(f"tg.name IN ({placeholders})")
            params.extend(tags)
        
        if completed is not None:
            conditions.append("t.completed = ?")
            params.append(completed)
        
        if priority:
            conditions.append("t.priority = ?")
            params.append(priority)
        
        if overdue_only:
            conditions.append("t.due_date < datetime('now')")
            conditions.append("t.completed = 0")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        # Sort: overdue first, then by priority, then by due date
        query += " ORDER BY t.completed ASC, t.priority DESC, t.due_date ASC"
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        if offset:
            query += " OFFSET ?"
            params.append(offset)
        
        cursor.execute(query, params)
        todo_ids = [row[0] for row in cursor.fetchall()]
        
        return [Todo.get_by_id(tid) for tid in todo_ids if Todo.get_by_id(tid)]
    
    def __str__(self) -> str:
        """String representation of TODO."""
        status = "✓" if self.completed else "☐"
        return f"{status} TODO #{self.id}: {self.title}"
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Todo(id={self.id}, title='{self.title}', priority='{self.priority}', completed={self.completed})"
