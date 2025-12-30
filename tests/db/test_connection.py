# -*- coding: utf-8 -*-
# tests/db/test_connection.py

import os
from unittest.mock import patch, MagicMock
from app.db.connection import db_connect, db_close

def test_db_connect():
    with patch.dict(
        os.environ,
        {"DB_NAME": "testdb",
         "DB_USER": "testuser",
         "DB_PASSWORD": "testpass",
         "DB_HOST": "localhost",
         "DB_PORT": "5432"}):

            with patch("app.db.connection.connect") as mock_connect:
                mock_conn = MagicMock()
                mock_connect.return_value = mock_conn

                conn = db_connect()

                mock_connect.assert_called_once_with(
                    dbname="testdb",
                    user="testuser",
                    password="testpass",
                    host="localhost",
                    port="5432",
                    cursor_factory=mock_connect.call_args \
                                               .kwargs["cursor_factory"]
                )

                assert conn is mock_conn
                assert conn.autocommit is False

def test_db_close_when_open():
    mock_conn = MagicMock()
    mock_conn.closed = False
    db_close(mock_conn)
    mock_conn.close.assert_called_once()

def test_db_close_when_closed():
    mock_conn = MagicMock()
    mock_conn.closed = True
    db_close(mock_conn)
    mock_conn.close.assert_not_called()
