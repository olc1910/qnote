#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qnote.core - Core functionality

This package contains the core business logic of qnote:
- Note: Note model and operations
- Snippet: Code snippet model and operations
- TODO: TODO/Task model and operations
- Database: Database connection and schema management

Copyright (c) 2026 Otis L. Crossley
Licensed under the MIT License.
"""

from qnote.core.database import Database
from qnote.core.note import Note
from qnote.core.snippet import Snippet
from qnote.core.todo import Todo

__all__ = ["Database", "Note", "Snippet", "Todo"]
