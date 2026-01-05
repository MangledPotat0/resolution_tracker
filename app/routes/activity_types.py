# -*- coding: utf-8 -*-
"""
app/router/activity_types.py

Defines the routes for workflow related to activity_types table.
"""

# 3rd party module imports
from flask import Blueprint, current_app, render_template, request, redirect, \
                  url_for

# local module imports
from app.db.activity_queries import delete_activity_type, get_activity_type, \
        get_all_activity_types, insert_activity_type, update_activity_type
from app.db.unit_queries import get_all_unit_groups, get_unit_group

activity_types_bp = Blueprint("activity_types", __name__)

@activity_types_bp.route("/action")
def activity_types_action_router():
    print("AAA")
    action = request.args.get("action")
    match action:
        case "create":
            return redirect(url_for("activity_types.create_activity"))
        case "view":
            return redirect(url_for("activity_types.view_activity_types"))
        case "update":
            return redirect(
                    url_for("activity_types.update_activity_type_start"))
        case "delete":
            return redirect(
                    url_for("activity_types.delete_activity_type_start"))
        case _:
            return "Invalid action", 400

@activity_types_bp.route("/create", methods=["GET", "POST"])
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

@activity_types_bp.route("/view", methods=["GET"])
def view_activity_types():
    conn = current_app.db
    activity_types = get_all_activity_types(conn)
    for i in range(len(activity_types)):
        activity_types[i]["unit_group_name"] = get_unit_group(
            conn, activity_types[i]["unit_group_id"])["name"] 
    return render_template("activity_types/view.html",
                           activity_types=activity_types)

@activity_types_bp.route("/update_start", methods=["GET"])
def update_activity_type_start():
    return manipulate_activity_type_start("update")

@activity_types_bp.route("/delete_start", methods=["GET"])
def delete_activity_type_start():
    return manipulate_activity_type_start("delete")

def manipulate_activity_type_start(action):
    conn = current_app.db
    activity_types = get_all_activity_types(conn)

    return render_template(
        f"activity_types/{action}.html",
        activity_types=activity_types,
        hx_get_url=f"/activity_types/{action}/get_activity_types",
        hx_target="#activity-types-dropdown"
    )

@activity_types_bp.route("/update/get_activity_types")
@activity_types_bp.route("/delete/get_activity_types")
def get_activity_types():
    conn = current_app.db
    activity_types = get_all_activity_types(conn)
    workflow = "/".join(request.path.split("/")[:3])
    match workflow:
        case "/activity_types/update":
            hx_get_url=f"{workflow}/get_activity_type_form"
            hx_target="#activity-type-update-form"
        case "/activity_types/delete":
            hx_get_url=f"{workflow}/get_activity_type_form"
            hx_target="#activity-type-delete-form"
        case _:
            raise ValueError(f"Unexpected worfklow: {workflow}")
    return render_template(
            "activity_types/partials/activity_types_dropdown.html",
            activity_types=activity_types,
            hx_get_url=hx_get_url,
            hx_target=hx_target
    )

@activity_types_bp.route("/update/get_activity_type_form")
def get_activity_update_form():
    activity_id = request.args.get("id")
    conn = current_app.db
    activity = get_activity_type(conn, activity_id)
    groups = get_all_unit_groups(conn)

    return render_template(
            "activity_types/partials/activity_type_update_form.html",
            activity=activity, groups=groups)

@activity_types_bp.route("/update/submit", methods=["POST"])
def update_activity_type_submit():
    conn = current_app.db
    activity_id = request.form.get("id")
    activity_name = request.form.get("name")
    unit_group_id = request.form.get("group_id")
    goal_quantity = request.form.get("goal_quantity")
    update_activity_type(conn, activity_id, activity_name, unit_group_id,
                      goal_quantity)

    return render_template("activity_types/update_result.html",
                           name=activity_name)

@activity_types_bp.route("/delete/get_activity_type_form")
def get_activity_delete_form():
    activity_id = request.args.get("id")
    conn = current_app.db
    activity = get_activity_type(conn, activity_id)

    return render_template(
            "activity_types/partials/activity_type_delete_form.html",
            act=activity)

@activity_types_bp.route("/delete/submit", methods=["POST"])
def delete_activity_type_submit():
    conn = current_app.db
    activity_id = request.form.get("id")
    activity_name = request.form.get("name")
    delete_activity_type(conn, activity_id)

    return render_template("activity_types/delete_result.html",
                           name=activity_name)

# EOF
