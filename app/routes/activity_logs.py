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

@activity_logs_bp.route("/action")
def activity_logs_action_router():
    action = request.args.get("action")
    match action:
        case "create":
            return redirect(url_for("activity_logs.create_activity"))
        case "view":
            return redirect(url_for("activity_logs.view_activity_logs"))
        case "update":
            return redirect(url_for("activity_logs.update_activity_log_start"))
        case "delete":
            return redirect(url_for("activity_logs.delete_activity_log_start"))
        case _:
            return "Invalid action", 400

@activity_logs_bp.route("/create", methods=["GET", "POST"])
def create_activity():
    conn = current_app.db
    if request.method == "POST":
        name = request.form.get("name")
        type_id = request.form.get("activity_type_id")
        quantity = request.form.get("quantity")

        activity_type_name = get_activity_type(conn, activity_type_id)["name"]
        try:
            if len(quantity) > 0:
                quantity = float(quantity)
            else:
                quantity = None
        except ValueError:
            return "quantity must be numbers."

        try:
            new_id = insert_activity_log(conn, group_id, name, quantity)
        except Exception as e:
            return f"Error creating activity: {e}"
        
        return render_template(
            "activity_logs/create_result.html",
            activity_id=new_id,
            name=name,
            group_name=group_name,
            quantity=quantity
        )

    groups = get_all_unit_groups(conn)
    return render_template("activity_logs/create.html", groups=groups)

@activity_logs_bp.route("/view", methods=["GET"])
def view_activity_logs():
    conn = current_app.db
    activity_logs = get_all_activity_logs(conn)
    for i in range(len(activity_logs)):
        activity_logs[i]["unit_group_name"] = get_unit_group(
            conn, activity_logs[i]["unit_group_id"])["name"] 
    return render_template("activity_logs/view.html",
                           activity_logs=activity_logs)

@activity_logs_bp.route("/update_start", methods=["GET"])
def update_activity_log_start():
    return manipulate_activity_log_start("update")

@activity_logs_bp.route("/delete_start", methods=["GET"])
def delete_activity_log_start():
    return manipulate_activity_log_start("delete")

def manipulate_activity_log_start(action):
    conn = current_app.db
    activity_logs = get_all_activity_logs(conn)

    return render_template(
        f"activity_logs/{action}.html",
        activity_logs=activity_logs,
        hx_get_url=f"/activity_logs/{action}/get_activity_logs",
        hx_target="#activity-types-dropdown"
    )

@activity_logs_bp.route("/update/get_activity_logs")
@activity_logs_bp.route("/delete/get_activity_logs")
def get_activity_logs():
    conn = current_app.db
    activity_logs = get_all_activity_logs(conn)
    workflow = "/".join(request.path.split("/")[:3])
    match workflow:
        case "/activity_logs/update":
            hx_get_url=f"{workflow}/get_activity_log_form"
            hx_target="#activity-type-update-form"
        case "/activity_logs/delete":
            hx_get_url=f"{workflow}/get_activity_log_form"
            hx_target="#activity-type-delete-form"
        case _:
            raise ValueError(f"Unexpected worfklow: {workflow}")
    return render_template(
            "activity_logs/partials/activity_logs_dropdown.html",
            activity_logs=activity_logs,
            hx_get_url=hx_get_url,
            hx_target=hx_target
    )

@activity_logs_bp.route("/update/get_activity_log_form")
def get_activity_update_form():
    activity_id = request.args.get("id")
    conn = current_app.db
    activity = get_activity_log(conn, activity_id)
    groups = get_all_unit_groups(conn)

    return render_template(
            "activity_logs/partials/activity_log_update_form.html",
            activity=activity, groups=groups)

@activity_logs_bp.route("/update/submit", methods=["POST"])
def update_activity_log_submit():
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
