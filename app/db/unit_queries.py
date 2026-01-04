# -*- coding: utf-8 -*-
"""
app/db/unit_queries.py

All the psql queries for database transactions related to units.
"""

# Built-in module imports
from typing import Any, Dict, Optional

# 3rd party module imports
from psycopg2.extensions import connection

# SQL strings for unit_groups table
GET_UNIT_GROUP = """
SELECT 
    ugroup.id,
    ugroup.name,
    unit.id AS canonical_unit_id,
    unit.name AS canonical_unit_name
FROM unit_groups ugroup
JOIN units unit
    ON ugroup.id = unit.group_id
WHERE ugroup.id = %s
    AND unit.is_canonical = true;
"""
INSERT_UNIT_GROUP = """
INSERT INTO unit_groups (name)
VALUES (%s)
RETURNING id;
"""
UPDATE_UNIT_GROUP = """
UPDATE unit_groups
SET name = %s
WHERE id = %s;
"""
DELETE_UNIT_GROUP = """
DELETE FROM unit_groups
WHERE id = %s;
"""

# SQL strings for units table
GET_UNIT = """
SELECT id, name, group_id, factor, shift, is_canonical
FROM units
WHERE id = %s;
"""
INSERT_UNIT = """
INSERT INTO units (name, group_id, factor, shift)
VALUES (%s, %s, %s, %s)
RETURNING id;
"""
UPDATE_UNIT = """
UPDATE units
SET
    name = %s,
    group_id = %s,
    factor = %s,
    shift = %s
WHERE id = %s;
"""
DELETE_UNIT = """
DELETE FROM units
WHERE id = %s;
"""

# SQL string to set canonical unit
SET_CANONICAL_UNIT = """
UPDATE units
SET is_canonical = true
WHERE id = %s;
"""

# Python wrappers for unit_groups table manipulation
def get_unit_group(conn: connection, group_id: int) -> Optional[Dict[str, Any]]:
    """
    Fetches a unit group by ID from unit_groups table.

    Args:
        conn (connection): Handle for psql database connection.
        group_id (int): id of the unit group to fetch.

    Returns:
        Optional[Dict[str, Any]]: Dict object from RealDictCursor containing
            record whose id matches the group_id. None if no match is found.
    """
    with conn.cursor() as cur:
        cur.execute(GET_UNIT_GROUP, (group_id,))
        return cur.fetchone()

def insert_unit_group(conn: connection, group_name: str,
        canonical_unit_name: str) -> int:
    """
    Inserts a unit group into the unit_groups table, inserts a unit into the
    units table whose group_id is the unit_group just created, and then sets
    that unit as the canonical unit for the unit_group. The canonical unit for
    a unit group may not be changed.

    Args:
        conn (connection): Handle for psql database connection.
        group_name (str): Name of the unit group to create.
        canonical_unit_name (str): Name of the canonical unit to create for
            the unit group.

    Returns:
        int: id assigned to the newly created unit_group record.
    """
    with conn.cursor() as cur:
        cur.execute(INSERT_UNIT_GROUP, (group_name,))
        group_id = cur.fetchone()["id"]
        cur.execute(
            INSERT_UNIT,
            (canonical_unit_name, group_id, 1, 0,)
        )
        unit_id = cur.fetchone()["id"]
        cur.execute(SET_CANONICAL_UNIT, (unit_id,))
    conn.commit()
    return group_id

def update_unit_group(conn: connection, group_id: int, name: str) -> None:
    """
    Updates a unit group in the unit_groups table.

    Args:
        conn (connection): Handle for psql database connection.
        group_id (int): id of the unit group to update.
        name (str): New name for the unit group.
    """
    with conn.cursor() as cur:
        cur.execute(
            UPDATE_UNIT_GROUP,
            (name, group_id,)
        )
    conn.commit()

def delete_unit_group(conn: connection, group_id: int) -> None:
    """
    Deletes a unit group in the unit_groups table.

    Args:
        conn (connection): Handle for psql database connection.
        group_id (int): id of the unit group to delete.
    """
    with conn.cursor() as cur:
        cur.execute(DELETE_UNIT_GROUP, (group_id,))
    conn.commit()

# Python_wrappers for units table manipulation
def get_unit(conn: connection, unit_id: int) -> Optional[Dict[str, Any]]:
    """
    Fetches a unit by ID from units table.

    Args:
        conn (connection): Handle for psql database connection.
        unit_id (int): ID of the unit to fetch from table.

    Returns:
        Optional[Dict[str, Any]]: Dict object from RealDictCursor containing
            record whose id matches the unit_id. None if no match is found.
    """
    with conn.cursor() as cur:
        cur.execute(GET_UNIT, (unit_id,))
        return cur.fetchone()

def insert_unit(conn: connection, name: str, group_id: int,
        factor: float, shift: float) -> int:
    """
    Inserts a unit into the units table.

    Args:
        conn (connection): Handle for psql database connection.
        name (str): Name of the unit.
        group_id (int): ID of unit group that the new unit belongs to.
        factor (float): Multiplicative factor when converting to the canonical
            unit.
        shift (float): Additive shift when converting to the canonical unit.

    Returns:
        int: id assigned to the newly created unit record.
    """
    with conn.cursor() as cur:
        cur.execute(
            INSERT_UNIT,
            (name, group_id, factor, shift,)
        )
        unit_id = cur.fetchone()["id"]
    conn.commit()
    return unit_id

def update_unit(conn: connection, unit_id: int, name: str, group_id: int,
        factor: float, shift: float) -> None:
    """
    Updates a unit in the units table.

    Args:
        conn (connection): Handle for psql database connection.
        unit_id (int): ID of the unit to update.
        name (str): New name of the unit.
        group_id (int): New ID of unit group that the new unit belongs to.
        factor (float): New multiplicative factor when converting to the
            canonical unit.
        shift (float): New additive shift when converting to the canonical
            unit.
    """
    with conn.cursor() as cur:
        cur.execute(
            UPDATE_UNIT,
            (name, group_id, factor, shift, unit_id,)
        )
    conn.commit()

def delete_unit(conn: connection, unit_id: int) -> None:
    """
    Deletes a unit in the units table.

    Args:
        conn (connection): Handle for psql database connection.
        unit_id (int): ID of the unit record to delete.
    """
    with conn.cursor() as cur:
        cur.execute(DELETE_UNIT, (unit_id,))
    conn.commit()

# EOF
