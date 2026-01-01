# -*- coding: utf-8 -*-
# tests/confttest.py

import os
import pytest
import psycopg2

TEST_DB_NAME = "testdb"
TEST_USER = "testuser"
TEST_PASSWORD = "testpass"
TEST_HOST = os.getenv("TEST_DB_HOST") or "testdb"
TEST_PORT = "5432"

print("REACHED FIXTURE DESTINATION")

@pytest.fixture(scope="session", autouse=True)
def set_test_db_env():
    os.environ["DB_NAME"] = TEST_DB_NAME
    os.environ["DB_USER"] = TEST_USER
    os.environ["DB_PASSWORD"] = TEST_PASSWORD
    os.environ["DB_HOST"] = TEST_HOST
    os.environ["DB_PORT"] = TEST_PORT

@pytest.fixture(scope="session")
def conn():
    conn = psycopg2.connect(
        dbname="postgres",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    yield conn
    conn.close()

@pytest.fixture(autouse=True)
def test_db(conn):
    with conn.cursor() as cur:
        try:
            cur.execute("TRUNCATE activity_logs RESTART IDENTITY CASCADE;")
            cur.execute("TRUNCATE activity_types RESTART IDENTITY CASCADE;")
        except psycopg2.errors.UndefinedTable:
            # Tables don't exist
            conn.rollback()
        else:
            conn.commit()

# EOF
