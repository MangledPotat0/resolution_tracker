# -*- coding: utf-8 -*-
# tests/db/test_activity_queries.py

import pytest

from app.db import activity_queries

def test_insert_andd_Get_activity_type(db_conn):
    queries.insert_activity_type(db_conn, "yoga", "minutes", 30)
    
    row = queries.get_activity_type(db_conn, 1)

    assert row is not None
