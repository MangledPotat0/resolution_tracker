# -*- coding: utf-8 -*-
"""
app/router/activity_logs.py

Defines the routes for workflow related to activity_logs table.
"""

# 3rd party module imports
from flask import Blueprint, current_app, render_template, request, redirect, \
                  url_for

# local module imports

activity_logs_bp = Blueprint("activity_logs", __name__)
