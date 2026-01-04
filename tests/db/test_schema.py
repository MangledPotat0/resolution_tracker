# -*- coding: utf-8 -*-
# tests/test_schema.py

print("TOP OF FILE")

import os
import pytest
import psycopg2
from psycopg2.extensions import connection
from app.db.schema import initialize_schema, table_exists

TEST_DB_NAME = "testdb"
TEST_USER = "testuser"
TEST_PASSWORD = "testpass"
TEST_HOST = os.getenv("TEST_DB_HOST") or "testdb"
TEST_PORT = "5432"

print("REACHED FIXTURE DESTINATION")

"""
@pytest.fixture(scope="module", autouse=True)
def set_test_db_env():
    os.environ["DB_NAME"] = TEST_DB_NAME
    os.environ["DB_USER"] = TEST_USER
    os.environ["DB_PASSWORD"] = TEST_PASSWORD
    os.environ["DB_HOST"] = TEST_HOST
    os.environ["DB_PORT"] = TEST_PORT
"""

def create_test_database(conn):
    conn = psycopg2.connect(
        dbname="postgres",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {TEST_DB_NAME};")
    cur.execute(f"CREATE DATABASE {TEST_DB_NAME};")

    cur.close()
    conn.close()

def drop_test_database(conn):
    conn = psycopg2.connect(
        dbname="postgres",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {TEST_DB_NAME};")

    cur.close()
    conn.close()

"""
def connect_test_db():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
"""

@pytest.fixture(scope="module")
def test_db(conn):
    create_test_database(conn)
    yield
    drop_test_database(conn)

def test_schema_initialization_create_tables(test_db, conn):
    initialize_schema(conn)

    assert table_exists(conn, "activity_types")
    assert table_exists(conn, "activity_logs")
