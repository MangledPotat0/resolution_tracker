# -*- coding: utf-8 -*-
"""
app/router/unit_groups.py

Defines the routes for workflow related to units table.
"""

# 3rd party module imports
from flask import Blueprint, current_app, render_template, request, redirect, \
                  url_for

# local module imports
from app.db.unit_queries import insert_unit_group

unit_groups_bp = Blueprint("unit_groups", __name__)

@unit_groups_bp.route("/action")
def unit_groups_action_router():
    action = request.args.get("action")
    match action:
        case "create":
            return redirect(url_for("unit_groups.create_unit_group"))
        case "view":
            return redirect(url_for("unit_groups.view_unit_group"))
        case "update":
            return redirect(url_for("unit_groups.update_unit_group"))
        case "delete":
            return redirect(url_for("unit_groups.delete_unit_group"))
        case _:
            return "Invalid action", 400

@unit_groups_bp.route("/create", methods=["GET", "POST"])
def create_unit_group():
    conn = current_app.db
    if request.method == "POST":
        group_name = request.form.get("group_name")
        canonical_unit_name = request.form.get("canonical_unit_name")

        try:
            new_id = insert_unit_group(conn, group_name, canonical_unit_name)
        except Exception as e:
            return f"Error creating unit group: {e}"

    return render_template("unit_groups/create.html")

# EOF
