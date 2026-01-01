# -*- coding: utf-8 -*-
"""
app/db/queries.py

All the psql queries for database transactions.
"""

# Built-in module imports
from typing import Optional, Tuple, Any

# 3rd party module imports
from psycopg2.extensions import connection

# Parametrized Query Strings

## Queries for activity_types
GET_ACTIVITY_TYPE = """
    SELECT id, name, canonical_unit, goal_quantity FROM activity_types
    WHERE id = %s;
"""
INSERT_ACTIVITY_TYPE = """
    INSERT INTO activity_types (name, canonical_unit, goal_quantity)
    VALUES (%s, %s, %s) RETURNING id;
"""
UPDATE_ACTIVITY_TYPE = """
    UPDATE activity_types SET
        name = %s,
        canonical_unit = %s,
        goal_quantity = %s
    WHERE id = %s;
"""
DELETE_ACTIVITY_TYPE = """
    DELETE FROM activity_types WHERE id = %s;
"""

## Queries for activity_log
GET_ACTIVITY_LOG = """
    SELECT id, activity_type_id, quantity, timestamp FROM activity_logs
    WHERE id = %s;
"""
INSERT_ACTIVITY_LOG = """
    INSERT INTO activity_logs (activity_type_id, quantity)
    VALUES (%s, %s) RETURNING id;
"""
UPDATE_ACTIVITY_LOG = """
    UPDATE activity_logs SET
        activity_type_id = %s,
        quantity =%s
    WHERE id = %s;
"""
DELETE_ACTIVITY_LOG = """
    DELETE FROM activity_logs WHERE id = %s;
"""

# Python function wrappers to sql strings

## activity_types
def get_activity_type(conn: connection, activity_type_id: str) \
        -> Optional[Tuple[Any, ...]]:
    """
    Fetches an activity type record from the database by activity_type_id.

    Args:
        conn (connection): Handle for psql database connection.
        activity_type_id (int): Unique identifier for activity_type of
            interest.

    Returns:
        Optional[Tuple[Any, ...]]: The single fetched row is returned as a
            tuple if exists. Otherwise None.
    """
    with conn.cursor() as cur:
        cur.execute(GET_ACTIVITY_TYPE, (activity_type_id,))
        row = cur.fetchone()
        return row

def insert_activity_type(conn: connection, name: str, canonical_unit: str,
        goal_quantity: int=None) -> None:
    """
    Insert a new activity type record to the database.

    Args:
        conn (connection): Handle for psql database connection.
        name (str): Name of the new activity type.
        canonical_unit (str): The unit of measure for the activity.
        goal_quantity (int): The goal for activity. Value is optional, if None
            then goal_quantity field of database is null.
    """

    with conn.cursor() as cur:
        cur.execute(
            INSERT_ACTIVITY_TYPE,
            (name, canonical_unit, goal_quantity,)
        )
    conn.commit()

def update_activity_type(conn: connection, activity_type_id: int,
        name: str=None, canonical_unit: str=None, goal_quantity:int = None) \
                -> None:
    """
    Updates an existing activity_type record with new attribute values.

    Args:
        conn (connection): Handle for psql database connection.
        activity_type_id (int): The id of the activity_type record that needs
            to be updated.
        name (str): New name given to the activity type.
        canonical_unit (str): New unit of measure for the activity type.
        goal_quantity (int): New goal for activity type. Value is optional, if
            None, then goal_quantity field of database is null.
    """
    with conn.cursor() as cur:
        cur.execute(
            UPDATE_ACTIVITY_TYPE,
            (name, canonical_unit, goal_quantity, activity_type_id,)
        )
    conn.commit()

def delete_activity_type(conn: connection, activity_type_id: int) -> None:
    """
    Deletes an existing activity_type record.

    Args:
        conn (connection): Handle for psql database connection.
        activity_type_id (int): The id of the activity_type record to delete.
    """
    
    with conn.cursor() as cur:
        cur.execute(DELETE_ACTIVITY_TYPE, (activity_type_id,))
    conn.commit()

## activity logs
def get_activity_log(conn: connection, log_id: str) \
        -> Optional[Tuple[Any, ...]]:
    """
    Fetches an activity log record from the database by log_id.

    Args:
        conn (connection): Handle for psql database connection.
        log_id (int): Unique identifier for a record of interest in
            activity_logs table.

    Returns:
        Optional[Tuple[Any, ...]]: The single fetched row is returned as a
            tuple if exists. Otherwise None.
    """
    with conn.cursor() as cur:
        cur.execute(GET_ACTIVITY_LOG, (log_id,))
        row = cur.fetchone()
        return row

def insert_activity_log(conn: connection, activity_type_id: int,
        quantity: int=None) -> None:
    """
    Insert a new activity type record to the database.

    Args:
        conn (connection): Handle for psql database connection.
        activity_type_id (int): The id of the activity being logged.
        quantity (int): The amount of activity performed, measured in the
            canonical unit of the activity.
    """

    with conn.cursor() as cur:
        cur.execute(
            INSERT_ACTIVITY_LOG,
            (activity_type_id, quantity,)
        )
    conn.commit()

def update_activity_log(conn: connection, log_id: int, activity_type_id: int,
        quantity:int) -> None:
    """
    Updates an existing activity_log record with new attribute values.

    Args:
        conn (connection): Handle for psql database connection.
        log_id (int): The id of the activity_log that needs to be updated.
        activity_type_id (int): The id of the activity_type for the activity
            being logged.
        quantity (int): The new quantity of activity being logged.
    """
    with conn.cursor() as cur:
        cur.execute(
            UPDATE_ACTIVITY_LOG,
            (activity_type_id, quantity, log_id,)
        )
    conn.commit()

def delete_activity_log(conn: connection, log_id: int) -> None:
    """
    Deletes an existing activity_log record.

    Args:
        conn (connection): Handle for psql database connection.
        log_id (int): The id of the activity_log record to delete.
    """
    
    with conn.cursor() as cur:
        cur.execute(DELETE_ACTIVITY_LOG, (log_id,))
    conn.commit()
# EOF
