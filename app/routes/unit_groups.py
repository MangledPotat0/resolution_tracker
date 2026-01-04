# -*- coding: utf-8 -*-
"""
app/router/unit_groups.py

Defines the routes for workflow related to units table.
"""

# 3rd party module imports
from flask import Blueprint, current_app, render_template, request, redirect, \
                  url_for

# local module imports
from app.db.unit_queries import delete_unit_group, get_all_unit_groups, \
        get_unit_group, insert_unit_group, update_unit_group

unit_groups_bp = Blueprint("unit_groups", __name__)

@unit_groups_bp.route("/action")
def unit_groups_action_router():
    action = request.args.get("action")
    match action:
        case "create":
            return redirect(url_for("unit_groups.create_unit_group"))
        case "view":
            return redirect(url_for("unit_groups.view_unit_groups"))
        case "update":
            return redirect(url_for("unit_groups.update_unit_group_start"))
        case "delete":
            return redirect(url_for("unit_groups.delete_unit_group_start"))
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

        return render_template(
            "unit_groups/create_result.html",
            group_id=new_id,
            group_name=group_name,
        )

    return render_template("unit_groups/create.html")

@unit_groups_bp.route("/view", methods=["GET"])
def view_unit_groups():
    conn = current_app.db
    groups = get_all_unit_groups(conn)
    return render_template("unit_groups/view.html", groups=groups)

@unit_groups_bp.route("/update_start", methods=["GET"])
def update_unit_group_start():
    return manipulate_unit_group_start("update")

@unit_groups_bp.route("/delete_start", methods=["GET"])
def delete_unit_group_start():
    return manipulate_unit_group_start("delete")

def manipulate_unit_group_start(action):
    conn = current_app.db
    unit_groups = get_all_unit_groups(conn)

    return render_template(
        f"unit_groups/{action}.html",
        unit_groups=unit_groups,
        hx_get_url=f"/unit_groups/{action}/get_unit_groups",
        hx_target="#unit-group-dropdown"
    )

@unit_groups_bp.route("/update/get_unit_groups")
@unit_groups_bp.route("/delete/get_unit_groups")
def get_unit_groups():
    conn = current_app.db
    unit_groups = get_all_unit_groups(conn)
    workflow = "/".join(request.path.split("/")[:3])
    match workflow:
        case "/unit_groups/update":
            hx_get_url=f"{workflow}/get_unit_group_form"
            hx_target="#unit-group-update-form"
        case "/unit_groups/delete":
            hx_get_url=f"{workflow}/get_unit_group_form"
            hx_target="#unit-group-delete-form"
        case _:
            raise ValueError(f"Unexpected worfklow: {workflow}")
    print(hx_get_url)
    return render_template("unit_groups/partials/unit_group_dropdown.html",
                           unit_groups=unit_groups,
                           hx_get_url=hx_get_url,
                           hx_target=hx_target
    )

@unit_groups_bp.route("/update/get_unit_group_form")
def get_unit_group_upate_form():
    group_id = request.args.get("id")
    conn = current_app.db
    group = get_unit_group(conn, group_id)

    return render_template("unit_groups/partials/unit_group_update_form.html",
                           group=group)

@unit_groups_bp.route("/delete/get_unit_group_form")
def get_unit_group_delete_form():
    group_id = request.args.get("id")
    conn = current_app.db
    group = get_unit_group(conn, group_id)

    return render_template("unit_groups/partials/unit_group_delete_form.html",
                           group=group)

@unit_groups_bp.route("/update/submit", methods=["POST"])
def update_unit_submit():
    conn = current_app.db
    group_id = request.form.get("id")
    group_name = request.form.get("name")
    update_unit_group(conn, group_id, group_name)

    return render_template("unit_groups/update_result.html", name=group_name)

@unit_groups_bp.route("/delete/submit", methods=["POST"])
def delete_unit_submit():
    conn = current_app.db
    group_id = request.form.get("id")
    group_name = request.form.get("name")
    delete_unit_group(conn, group_id)

    return render_template("unit_groups/delete_result.html", name=group_name)

# EOF
