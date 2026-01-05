# -*- coding: utf-8 -*-
"""
app/db/activity_queries.py

All the psql queries for database transactions related to activities.
"""

# Built-in module imports
from typing import Any, Dict, List, Optional

# 3rd party module imports
from psycopg2.extensions import connection

# Parametrized Query Strings

## Queries for activity_types
GET_ACTIVITY_TYPE = """
SELECT
    type.id,
    type.name,
    type.unit_id,
    ug.name AS unit_group,
    type.goal_quantity
FROM activity_types type
JOIN unit_groups ug ON type.unit_id = ug.id
WHERE type.id = %s;
"""
GET_ALL_ACTIVITY_TYPES = """
SELECT id, name, unit_id, goal_quantity
FROM activity_types;
"""
INSERT_ACTIVITY_TYPE = """
INSERT INTO activity_types (name, unit_id, goal_quantity)
VALUES (%s, %s, %s) RETURNING id;
"""
UPDATE_ACTIVITY_TYPE = """
UPDATE activity_types
SET
    name = %s,
    unit_id = %s,
    goal_quantity = %s
WHERE id = %s;
"""
DELETE_ACTIVITY_TYPE = """
DELETE FROM activity_types WHERE id = %s;
"""

## Queries for activity_log
GET_ACTIVITY_LOG = """
SELECT
    act.id,
    act.activity_type_id,
    act.canonical_quantity,
    act.timestamp,
    disp.id AS display_unit_id,
    disp.name AS display_unit_name,
    act.canonical_quantity / disp.factor AS display_quantity
FROM activity_logs act
JOIN activity_types type ON act.activity_type_id = type.id
JOIN units disp ON disp.id = %s
WHERE act.id = %s;
"""
INSERT_ACTIVITY_LOG = """
INSERT INTO activity_logs (activity_type_id, canonical_quantity)
SELECT
    %s AS activity_type_id,
    %s * unit.factor AS canonical_quantity
FROM units unit
WHERE unit.id = %s
RETURNING id;
"""
UPDATE_ACTIVITY_LOG = """
UPDATE activity_logs as act
SET
    activity_type_id = %s,
    canonical_quantity = %s * unit.factor
FROM units unit
WHERE unit.id = %s
AND act.id = %s;
"""
DELETE_ACTIVITY_LOG = """
DELETE FROM activity_logs WHERE id = %s;
"""
GET_ACTIVITY_LOGS_FOR_TYPE = """
SELECT
    act.id,
    act.activity_type_id,
    act.canonical_quantity,
    act.timestamp,
    disp.id AS display_unit_id,
    disp.name AS display_unit_name,
    act.canonical_quantity / disp.factor AS display_quantity
FROM activity_logs act
JOIN activity_types type ON act.activity_type_id = type.id
JOIN units disp ON disp.id = %s
WHERE act.activity_type_id = %s;
"""

# Python function wrappers to sql strings

## activity_types
def get_activity_type(conn: connection, activity_type_id: int) \
        -> Optional[Dict[str, Any]]:
    """
    Fetches an activity type record from the database by activity_type_id.

    Args:
        conn (connection): Handle for psql database connection.
        activity_type_id (int): Unique identifier for activity_type of
            interest.

    Returns:
        Optional[Dict[str, Any]]: The single fetched row is returned as a
            tuple if exists. Otherwise None.
    """
    with conn.cursor() as cur:
        cur.execute(GET_ACTIVITY_TYPE, (activity_type_id,))
        row = cur.fetchone()
        return row

def insert_activity_type(conn: connection, unit_id: int, name: str,
        goal_quantity: float=None) -> None:
    """
    Insert a new activity type record to the database.

    Args:
        conn (connection): Handle for psql database connection.
        name (str): Name of the new activity type.
        unit_id (int): The unit group of measure for the activity.
        goal_quantity (int): The goal for activity. Value is optional, if None
            then goal_quantity field of database is null.
    """

    with conn.cursor() as cur:
        cur.execute(
            INSERT_ACTIVITY_TYPE,
            (name, unit_id, goal_quantity,)
        )
        activity_type_id = cur.fetchone()["id"]
    conn.commit()
    return activity_type_id

def update_activity_type(conn: connection, activity_type_id: int, name: str,
        unit_id: int, goal_quantity:int = None) -> None:
    """
    Updates an existing activity_type record with new attribute values.

    Args:
        conn (connection): Handle for psql database connection.
        activity_type_id (int): The id of the activity_type record that needs
            to be updated.
        name (str): New name given to the activity type.
        unit_id (int): New unit group of measure for the activity type.
        goal_quantity (int): New goal for activity type. Value is optional, if
            None, then goal_quantity field of database is null.
    """
    with conn.cursor() as cur:
        cur.execute(
            UPDATE_ACTIVITY_TYPE,
            (name, unit_id, goal_quantity, activity_type_id,)
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
def get_activity_log(conn: connection, display_unit_id: int, log_id: str) \
        -> Optional[Dict[str, Any]]:
    """
    Fetches an activity log record from the database by log_id.

    Args:
        conn (connection): Handle for psql database connection.
        display_unit_id (int): ID corresponding to the user specified display
            quantity for the record being requested.
        log_id (int): Unique identifier for a record of interest in
            activity_logs table.

    Returns:
        Optional[Dict[str, Any]]: The single fetched row is returned as a
            tuple if exists. Otherwise None.
    """
    with conn.cursor() as cur:
        cur.execute(GET_ACTIVITY_LOG, (display_unit_id, log_id,))
        row = cur.fetchone()
        return row

def insert_activity_log(conn: connection, activity_type_id: int,
        quantity: float, unit_id: int) -> None:
    """
    Insert a new activity type record to the database.

    Args:
        conn (connection): Handle for psql database connection.
        activity_type_id (int): The id of the activity being logged.
        quantity (int): The amount of activity performed, measured in user
                specified unit.
        unit_id (int): The id of the unit for the quantity entered.
    """

    with conn.cursor() as cur:
        cur.execute(
            INSERT_ACTIVITY_LOG,
            (activity_type_id, quantity, unit_id)
        )
    conn.commit()

def update_activity_log(conn: connection, log_id: int, activity_type_id: int,
        quantity: float, unit_id: int) -> None:
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
            (activity_type_id, quantity, unit_id, log_id,)
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

def get_all_activity_types(conn: connection) -> List[Dict[str, Any]]:
    """
    Fetches all the activity types saved on activity_types table.

    Args:
        conn (connection): Handle for psql database connection.

    Returns:
        List[Dict[str, Any]]: List of RealDictCursor dict objects containing
            the records of activity_types table.
    """

    with conn.cursor() as cur:
        cur.execute(GET_ALL_ACTIVITY_TYPES)
        return cur.fetchall()

def get_activity_logs_for_type(conn: connection, display_unit_id: int,
        activity_type_id: int) -> List[Dict[str, Any]]:
    """
    Fetches all the activity log records matching the specified
    activity_type_id.

    Args:
        conn (connection): Handle for psql database connection.
        display_unit_id (int): unit_id value of the user's specified unit for
            presenting the values.
        activity_type_id (int): ID value for the activity of interest.

    Returns:
        List[Dict[str, Any]]: List object of dictionaries as formatted by
            RealDictCursor.
    """
    with conn.cursor() as cur:
        cur.execute(GET_ACTIVITY_LOGS_FOR_TYPE,
                    (display_unit_id, activity_type_id,))
        return cur.fetchall()
# EOF
