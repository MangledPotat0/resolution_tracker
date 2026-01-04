# -*- coding: utf-8 -*-
"""
app/router/units.py

Defines the routes for workflow related to units table.
"""

# 3rd party module imports
from flask import Blueprint, current_app, render_template, request, redirect, \
                  url_for

# local module imports
from app.db.unit_queries import get_all_units, get_all_unit_groups, get_unit, \
        get_all_units_by_group, insert_unit, update_unit

units_bp = Blueprint("units", __name__)

@units_bp.route("/action")
def units_action_router():
    action = request.args.get("action")
    match action:
        case "create":
            return redirect(url_for("units.create_unit"))
        case "view":
            return redirect(url_for("units.view_units"))
        case "update":
            return redirect(url_for("units.update_unit_start"))
        case "":
            return redirect(url_for("units.delete_unit"))
        case _:
            return "Invalid action", 400

@units_bp.route("/create", methods=["GET", "POST"])
def create_unit():
    conn = current_app.db
    if request.method == "POST":
        name = request.form.get("name")
        group_id = request.form.get("group_id")
        factor = request.form.get("factor")
        shift = request.form.get("shift")

        try:
            factor = float(factor)
            shift = float(shift)
        except ValueError:
            return "Factor and shift must be numbers."

        try:
            new_id = insert_unit(conn, name, group_id, factor, shift)
        except Exception as e:
            return f"Error creating unit: {e}"
        
        return render_template(
            "units/create_result.html",
            unit_id=new_id,
            name=name,
            group_id=group_id,
            factor=factor,
            shift=shift
        )

    groups = get_all_unit_groups(conn)
    return render_template("units/create.html", groups=groups)

@units_bp.route("/view", methods=["GET"])
def view_units():
    conn = current_app.db
    units = get_all_units(conn)
    return render_template("units/view.html", units=units)

@units_bp.route("/update_unit", methods=["GET"])
def update_unit_start():
    conn = current_app.db
    groups = get_all_unit_groups(conn)
    return render_template("units/update.html", groups=groups)

@units_bp.route("/update/get_units")
def get_units_for_group():
    group_id = request.args.get("group_id")
    conn = current_app.db
    units = get_all_units_by_group(conn, group_id)
    return render_template("units/partials/unit_dropdown.html", units=units)

@units_bp.route("/update/get_unit_form")
def get_unit_form():
    unit_id = request.args.get("unit_id")
    conn = current_app.db
    unit = get_unit(conn, unit_id)
    groups = get_all_unit_groups(conn)

    return render_template("units/partials/unit_update_form.html",
                           unit=unit, groups=groups)

@units_bp.route("/update", methods=["POST"])
def update_unit_route():
    conn = current_app.db

    unit_id = request.form["unit_id"]
    name = request.form["name"]
    group_id = request.form["group_id"]
    factor = float(request.form["factor"])
    shift = float(request.form["shift"])

    update_unit(conn, unit_id, name, group_id, factor, shift)

    return render_template("units/update_result.html", name=name)

def delete_unit_route():
    conn = current_app.db
    # TODO

# EOF
