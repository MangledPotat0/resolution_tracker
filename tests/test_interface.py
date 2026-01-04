# -*- coding: utf-8 -*-
"""
tests/test_interface.py
"""

import pytest
from app.interface import create_app
from unittest.mock import patch

@pytest.fixture
def client(conn):
    with patch("app.interface.db_connect", return_value=conn):
        app = create_app()
        app.config["TESTING"] = True
        return app.test_client()

def test_home_render(client):
    response = client.get("/")
    assert response.status_code == 200 # HTTP CODE 200 == "OK"

# EOF
