# -*- coding: utf-8 -*-
"""
app/router/activity_types.py

Defines the routes for workflow related to activity_types table.
"""

# 3rd party module imports
from flask import Blueprint, current_app, render_template, request, redirect, \
                  url_for

# local module imports
from app.db.activity_queries import get_all_activity_types, \
        insert_activity_type
from app.db.unit_queries import get_all_unit_groups, get_unit_group

activities_bp = Blueprint("activities", __name__)

@activities_bp.route("/action")
def activities_action_router():
    print("AAA")
    action = request.args.get("action")
    match action:
        case "create":
            return redirect(url_for("activities.create_activity"))
        case "view":
            return redirect(url_for("activities.view_activities"))
        case "update":
            return redirect(url_for("activities.update_activity_type_start"))
        case "delete":
            return redirect(url_for("activities.delete_activity_type_start"))
        case _:
            return "Invalid action", 400

@activities_bp.route("/create", methods=["GET", "POST"])
def create_activity():
    conn = current_app.db
    if request.method == "POST":
        name = request.form.get("name")
        group_id = request.form.get("group_id")
        goal_quantity = request.form.get("goal_quantity")

        group_name = get_unit_group(conn, group_id)["name"]
        try:
            if len(goal_quantity) > 0:
                goal_quantity = float(goal_quantity)
            else:
                goal_quantity = None
        except ValueError:
            return "goal_quantity must be numbers."

        try:
            new_id = insert_activity_type(conn, group_id, name, goal_quantity)
        except Exception as e:
            return f"Error creating activity: {e}"
        
        return render_template(
            "activity_types/create_result.html",
            activity_id=new_id,
            name=name,
            group_name=group_name,
            goal_quantity=goal_quantity
        )

    groups = get_all_unit_groups(conn)
    return render_template("activity_types/create.html", groups=groups)

@activities_bp.route("/view", methods=["GET"])
def view_activities():
    conn = current_app.db
    activities = get_all_activity_types(conn)
    for i in range(len(activities)):
        activities[i]["unit_name"] = get_unit_group(
            conn, activities[i]["unit_id"])["name"] 
    return render_template("activity_types/view.html", activities=activities)

@activities_bp.route("/update_start", methods=["GET"])
def update_activity_type_start():
    return manipulate_activity_type_start("update")

@activities_bp.route("/delete_start", methods=["GET"])
def delete_activity_type_start():
    return manipulate_activity_type_start("delete")

def manipulate_activity_type_start(action):
    conn = current_app.db
    activity_types = get_all_activity_types(conn)

    return render_template(
        f"activity_types/{action}.html",
        activity_types=activity_types,
        hx_get_url=f"/activity_types/{action}/get_activity_types",
        hx_target="#activity-type-dropdown"
    )


# EOF
