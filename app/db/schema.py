# -*- coding: utf-8 -*-
"""
app/db/schema.py
Handles database table creation and management
"""

# 3rd party imports
from psycopg2.extensions import connection

# Table creation strings

CREATE_ACTIVITY_TYPES_TABLE = """
CREATE TABLE IF NOT EXISTS activity_types (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    unit_id INTEGER NOT NULL REFERENCES units(id) ON DELETE CASCADE,
    goal_quantity DOUBLE PRECISION
);
"""

CREATE_ACTIVITY_LOGS_TABLE = """
CREATE TABLE IF NOT EXISTS activity_logs (
    id SERIAL PRIMARY KEY,
    activity_type_id INTEGER NOT NULL REFERENCES activity_types(id),
    canonical_quantity DOUBLE PRECISION NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW()
);
"""

CREATE_UNIT_GROUPS_TABLE = """
CREATE TABLE IF NOT EXISTS unit_groups (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
);
"""

CREATE_UNITS_TABLE = """
CREATE TABLE IF NOT EXISTS units (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    group_id INTEGER NOT NULL REFERENCES unit_groups(id) ON DELETE CASCADE,
    factor DOUBLE PRECISION NOT NULL CHECK (factor > 0),
    offset DOUBLE PRECISION DEFAULT 0,
    is_canonical BOOLEAN NOT NULL DEFAULT FALSE
);
"""

UNIQUE_INDEX_RULE = """
CREATE UNIQUE INDEX one_canonical_per_group
ON units(group_id)
WHERE is_canonical = TRUE;
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
            ) as exists;
            """,
            (table_name,)
        )
        return cur.fetchone()["exists"]

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

def index_exists(conn: connection, index_name: str) -> bool:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT EXISTS (
                SELECT 1
                FROM pg_indexes
                WHERE schemaname = 'public'
                AND indexname = %s
            ) AS exists;
        """, (index_name,))
        return cur.fetchone()["exists"]

def create_index(conn: connection, index_name: str, index_sql: str) -> None:
    """
    Create a index that apply to the database.

    Args:
        conn (connection): psql database connection handle.
        index_sql (str): sql string to apply the trigger.
    """
    if index_exists(conn, index_name):
        print(f"Index {index_name} already exists.")
        return
    with conn.cursor() as cur:
        cur.execute(index_sql)
    conn.commit()
    print(f"Index {index_name }created")

def initialize_schema(conn) -> None:
    """
    Ensures that all required tables exist. It should be called once at
    service initialization step.

    Args:
        conn (connection): psql connection handle.
    """

    create_table(conn, "unit_groups", CREATE_UNIT_GROUPS_TABLE)
    create_table(conn, "units", CREATE_UNITS_TABLE)
    create_table(conn, "activity_types", CREATE_ACTIVITY_TYPES_TABLE)
    create_table(conn, "activity_logs", CREATE_ACTIVITY_LOGS_TABLE)
    create_index(conn, "one_canonical_per_group", UNIQUE_INDEX_RULE)

# EOF
