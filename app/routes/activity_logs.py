# -*- coding: utf-8 -*-
"""
app/router/activity_logs.py

Defines the routes for workflow related to activity_logs table.
"""

# 3rd party module imports
from flask import Blueprint, current_app, render_template, request, redirect, \
                  url_for

# local module imports
from app.db.activity_queries import delete_activity_log, \
        get_activity_logs_for_type, get_activity_log, get_activity_type, \
        get_all_activity_types, insert_activity_log, update_activity_log
from app.db.unit_queries import get_all_units_by_group, get_all_unit_groups, \
        get_unit, get_unit_group

activity_logs_bp = Blueprint("activity_logs", __name__)

# -------------------------------- ENTRY POINT --------------------------------

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

# ------------------------------- SHARED ROUTES -------------------------------

@activity_logs_bp.route("/create/units")
@activity_logs_bp.route("/view/units")
@activity_logs_bp.route("/update/units")
def units_dropdown():
    conn = current_app.db
    activity_type_id = request.args.get("activity_type_id")
    hx_get_url = request.args.get("hx_get_url")
    hx_target = request.args.get("hx_target")

    if not activity_type_id:
        units = []
    else:
        activity_type = get_activity_type(conn, activity_type_id)
        allowed_units = get_all_units_by_group(
                conn,
                activity_type["unit_group_id"]
        )
    return render_template(
            "activity_logs/partials/units_dropdown.html",
            hx_get_url=hx_get_url,
            hx_target=hx_target,
            units=allowed_units,
    )

@activity_logs_bp.route("/activity_logs")
def activity_logs_dropdown():
    conn = current_app.db
    activity_type_id = request.args.get("activity_type_id")
    hx_get_url = request.args.get("hx_get_url")
    hx_target = request.args.get("hx_target")

    if not activity_type_id:
        units = []
    else:
        ugroup_id = get_activity_type(conn, activity_type_id)["unit_group_id"]
        display_unit_id = get_unit_group(conn, ugroup_id)["canonical_unit_id"]
        activity_logs = get_activity_logs_for_type(
                conn,
                display_unit_id,
                activity_type_id
        )
    return render_template(
            "activity_logs/partials/activity_logs_dropdown.html",
            hx_get_url=hx_get_url,
            hx_target=hx_target,
            activity_logs=activity_logs,
            activity_type_id = activity_type_id
    )

# ------------------------------- CREATE ROUTES -------------------------------

@activity_logs_bp.route("/create", methods=["GET", "POST"])
def create_activity():
    conn = current_app.db
    activity_types = get_all_activity_types(conn)
    if request.method == "POST":
        activity_type_id = request.form["activity_type_id"]
        unit_id = request.form["unit_id"]
        quantity = request.form["quantity"]
        
        activity_id = insert_activity_log(
                conn, activity_type_id, quantity, unit_id
        )
        activity = get_activity_log(conn, unit_id, activity_id)
        
        return render_template(
                "activity_logs/create_result.html",
                activity=activity
        )

    return render_template(
            "activity_logs/create.html",
            activity_types=activity_types,
    )

# ------------------------------- VIEW ROUTES  -------------------------------

@activity_logs_bp.route("/view", methods=["GET"])
def view_activity_logs():
    conn = current_app.db
    activity_types = get_all_activity_types(conn)
    return render_template(
            "activity_logs/view.html",
            activity_types=activity_types,
    )

@activity_logs_bp.route("/view/table")
def view_activity_log_table():
    conn = current_app.db
    activity_type_id = request.args.get("activity_type_id")
    unit_id = request.args.get("unit_id")
    unit_name = get_unit(conn, unit_id)["name"]

    if not activity_type_id or not unit_id:
        logs = []
    else:
        logs = get_activity_logs_for_type(
            conn,
            unit_id,
            activity_type_id
        )
        for i in range(len(logs)):
            logs[i]["activity_type_name"] = get_activity_type(
                    conn, activity_type_id)["name"]

    return render_template(
        "activity_logs/partials/view_table.html",
        logs=logs,
        unit_name=unit_name
    )

# ------------------------------- UPDATE ROUTES -------------------------------

@activity_logs_bp.route("/update_start", methods=["GET"])
def update_activity_log_start():
    conn = current_app.db
    activity_types = get_all_activity_types(conn)
    return render_template(
            "activity_logs/update.html",
            activity_types=activity_types,
    )

@activity_logs_bp.route("/update_form")
def get_activity_update_form():
    conn = current_app.db
    activity_id = request.args.get("id")
    activity_type_id = request.args.get("activity_type_id")
    ugroup_id = get_activity_type(conn, activity_type_id)["unit_group_id"]
    units = get_all_units_by_group(conn, ugroup_id)
    canonical_unit_id = get_unit_group(conn, ugroup_id)["canonical_unit_id"]
    activity = get_activity_log(conn, canonical_unit_id, activity_id)

    return render_template(
            "activity_logs/partials/activity_log_update_form.html",
            activity=activity,
            units=units)

@activity_logs_bp.route("/update/submit", methods=["POST"])
def update_activity_log_submit():
    conn = current_app.db
    activity_type_id = request.form.get("activity_type_id")
    log_id = request.form.get("log_id")
    unit_id = request.form.get("unit_id")
    display_quantity = request.form.get("display_quantity")
    update_activity_log(conn, log_id, activity_type_id, display_quantity,
                        unit_id)

    return render_template("activity_logs/update_result.html", log_id=log_id)

# ------------------------------- DELETE ROUTES -------------------------------

@activity_logs_bp.route("/delete_start", methods=["GET"])
def delete_activity_log_start():
    conn = current_app.db
    activity_types = get_all_activity_types(conn)
    return render_template(
            "activity_logs/delete.html",
            activity_types=activity_types,
    )

@activity_logs_bp.route("/delete_form")
def get_activity_delete_form():
    conn = current_app.db
    activity_id = request.args.get("id")
    activity_type_id = request.args.get("activity_type_id")
    ugroup_id = get_activity_type(conn, activity_type_id)["unit_group_id"]
    units = get_all_units_by_group(conn, ugroup_id)
    canonical_unit_id = get_unit_group(conn, ugroup_id)["canonical_unit_id"]
    activity = get_activity_log(conn, canonical_unit_id, activity_id)

    return render_template(
            "activity_logs/partials/activity_log_delete_form.html",
            act=activity)

@activity_logs_bp.route("/delete/submit", methods=["POST"])
def delete_activity_log_submit():
    conn = current_app.db
    log_id = request.form.get("log_id")
    delete_activity_log(conn, log_id)

    return render_template("activity_logs/delete_result.html",
                           log_id=log_id)

# EOF
