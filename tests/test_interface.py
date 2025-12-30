# -*- coding: utf-8 -*-
"""
tests/test_interface.py
"""

import pytest
from app.interface import create_app

@pytest.fixture
def client():
    app = create_app()
    return app.test_client()

def test_home_render(client):
    response = client.get("/")
    assert response.status_code == 200 # HTTP CODE 200 == "OK"
    assert b"yoga" in response.data
    assert b"push ups" in response.data

def test_invalid_goal(client):
    response = client.post("/process",
                           data={"goal": "potato",
                                 "number": "10"})
    assert response.status_code == 200
    assert b"Invalid Goal Selected" in response.data

def test_invalid_number(client):
    response = client.post("/process",
                           data={"goal": "yoga",
                                 "number": "abc"})
    assert response.status_code == 200
    assert b"Please enter a number." in response.data

def test_valid_submission(client):
    response = client.post("/process",
                           data={"goal": "yoga",
                                 "number": "10"})
    assert response.status_code == 200
    assert b"You have completed 10 minutes of yoga." in response.data
