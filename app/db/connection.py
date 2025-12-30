# -*- coding: utf-8 -*-
"""
connection.py
Establishes connection to the postgreSQL database that stores all the data
entries.
"""

# built-in module imports
import os

# 3rd party module imports
from psycopg2 import connect
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor

def db_connect() -> connection:
    """
    Establish a pg2 connection and return the connection.

    Returns:
        connection handle to postgres database.
    """

    conn = connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            cursor_factory=RealDictCursor
    )
    
    conn.autocommit = False
    
    return conn

def db_close(conn: connection) -> None:
    """
    Close the connection to database.
    """
    if conn and not conn.closed:
        conn.close()


# EOF
