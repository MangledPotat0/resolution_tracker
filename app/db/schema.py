# -*- coding: utf-8 -*-
"""
app/db/schema.py
Handles database table creation and management
"""

# 3rd party imports
import psycopg2 as pg
from psycopg2 import sql
from psycopg2.extensions import connection

# Table creation strings

CREATE_ACTIVITY_TYPES_TABLE = """
CREATE TABLE activity_types (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    canonical_unit TEXT NOT NULL,
    goal_quantity NUMERIC
);
"""

CREATE_ACTIVITY_LOGS_TABLE = """
CREATE TABLE activity_logs (
    id SERIAL PRIMARY KEY,
    activity_type_id INTEGER NOT NULL REFERENCES activity_types(id),
    quantity NUMERIC NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW()
);
"""

def table_exists(conn: connection, table_name: str) -> bool:
    """
    Checks whether or not specified table exists in the database connected to
    the current connection handle.

    Args:
        conn (connection): psql database connection handle.
        table_name (str): Name of the table being checked.

    Returns:
        
    """
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = %s
            );
            """,
            (table_name,)
        )
        return cur.fetchone()[0]

def create_table(conn: connection, table_name: str, create_sql: str) -> None:
    """
    Checks for table in the database. if it exists, nothing happens. If it
    doesn't, then creates the table.

    Args:
        conn (connection): psql database connection handle.
        table_name (str): Name of the table to create.
        create_sql (str): sql query string to create the table.

    Returns:
        None
    """
    if table_exists(conn, table_name):
        print(f"Table \"{table_name}\" already exists.")
        return

    print(f"Table \"{table_name}\" does not exist. Creating it now.")
    with conn.cursor() as cur:
        cur.execute(create_sql)
    conn.commit()
    print(f"Table \"{table_name}\" created.")

def initialize_schema(conn) -> None:
    """
    Ensures that all required tables exist. It should be called once at
    service initialization step.

    Args:
        conn (connection): psql connection handle.
    """

    create_table(conn, "activity_types", CREATE_ACTIVITY_TYPES_TABLE)
    create_table(conn, "activity_logs", CREATE_ACTIVITY_LOGS_TABLE)

# EOF
