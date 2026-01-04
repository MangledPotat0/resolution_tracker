# -*- coding: utf-8 -*-
"""
app/router/activity_types.py

Defines the routes for workflow related to activity_types table.
"""

# 3rd party module imports
from flask import Blueprint, current_app, render_template, request, redirect, \
                  url_for

# local module imports
from app.db.activity_queries import

activities_bp = Blueprint("activities", __name__)

@activities_bp.route("/action")
def activities_action_router():
    action = request.args.get("action")
    match action:
        case "create":
            return redirect(url_for("activities.create_activity"))
        case "view":
            return redirect(url_for("activities.view_activities"))
        case "update":
            return redirect(url_for("activities.update_activity_start"))
        case "delete":
            return redirect(url_for("activities.delete_activity_start"))
        case _:
            return "Invalid action", 400
