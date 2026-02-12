#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Note model

Copyright (c) 2026 [Dein Name]
Licensed under the MIT License.
"""

import pytest
from pathlib import Path
import tempfile

from qnote.core.note import Note
from qnote.core.database import Database, get_database


@pytest.fixture
def test_db():
    """Create a temporary test database."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = Path(tmp.name)
    
    # Initialize test database
    db = Database(db_path)
    
    yield db
    
    # Cleanup
    db.close()
    db_path.unlink()


def test_create_note(test_db):
    """Test creating a new note."""
    note = Note(
        content="Test note content",
        title="Test Note",
        tags=["test", "example"]
    )
    
    note.save()
    
    assert note.id is not None
    assert note.created_at is not None
    assert note.updated_at is not None
    assert note.content == "Test note content"
    assert note.title == "Test Note"
    assert "test" in note.tags
    assert "example" in note.tags


def test_get_note_by_id(test_db):
    """Test retrieving a note by ID."""
    # Create a note
    note = Note(content="Test content", title="Test").save()
    note_id = note.id
    
    # Retrieve it
    retrieved = Note.get_by_id(note_id)
    
    assert retrieved is not None
    assert retrieved.id == note_id
    assert retrieved.content == "Test content"
    assert retrieved.title == "Test"


def test_update_note(test_db):
    """Test updating an existing note."""
    # Create a note
    note = Note(content="Original content").save()
    note_id = note.id
    
    # Update it
    note.content = "Updated content"
    note.title = "Updated Title"
    note.save()
    
    # Retrieve and verify
    updated = Note.get_by_id(note_id)
    assert updated.content == "Updated content"
    assert updated.title == "Updated Title"


def test_delete_note(test_db):
    """Test deleting a note."""
    # Create a note
    note = Note(content="To be deleted").save()
    note_id = note.id
    
    # Delete it
    note.delete()
    
    # Verify it's gone
    retrieved = Note.get_by_id(note_id)
    assert retrieved is None


def test_empty_content_raises_error(test_db):
    """Test that empty content raises ValueError."""
    note = Note(content="")
    
    with pytest.raises(ValueError):
        note.save()


# TODO: Add more tests
# - Test tag filtering
# - Test search functionality
# - Test starred notes
# - Test pagination
# - Test sorting
