# -*- coding: utf-8 -*-
"""
app/interface.py
This module controls and provides the rendering of the web app that is served
to the user.
"""
# 3rd party module imports
from flask import Flask, render_template, request

# local module imports
from app.db.connection import db_connect, db_close
from app.db.schema import initialize_schema
from app.routes.units import units_bp
from app.routes.unit_groups import unit_groups_bp
from app.routes.activity_types import activity_types_bp
from app.routes.activity_logs import activity_logs_bp

def create_app() -> Flask:
    """
    Factory method to create the web app. The run.py entrypoint invokes this
    method once.

    Returns:
        Flask app object
    """
    app = Flask(__name__)
    app.register_blueprint(units_bp, url_prefix="/units")
    app.register_blueprint(unit_groups_bp, url_prefix="/unit_groups")
    app.register_blueprint(activity_types_bp, url_prefix="/activity_types")
    app.register_blueprint(activity_logs_bp, url_prefix="/activity_logs")
    try:
        app.db = db_connect()
        initialize_schema(app.db)
    except Exception as e:
        raise RuntimeError("Database connection failed") from e
    print("Connection opened for postgreSQL database")

    goals = {"yoga":" minutes",
             "push ups":" reps",
             "pull ups":" reps",
             "cycling":" km"}

    @app.route("/")
    def home():
        """
        Render the default home page.
        """
        return render_template("index.html", goals=list(goals.keys()))

    @app.route("/menu")
    def table_menu():
        table = request.args.get("table")
        print(table)
        match table:
            case "units":
                return render_template("/menu/units_menu.html")
            case "unit_groups":
                return render_template("/menu/unit_groups_menu.html")
            case "activity_types":
                return render_template("/menu/activity_types_menu.html")
            case "activity_logs":
                return render_template("/menu/activity_logs_menu.html")
            case _:
                return "Invalid table selection", 400

    @app.route("/process", methods=["POST"])
    def process():
        """
        Take user input and render the results.
        """
        goal = request.form.get("goal", "")
        number_raw = request.form.get("number", "")

        if goal not in goals:
            return render_template(
                "result.html",
                message="Invalid Goal Selected"
            )

        try:
            number = int(number_raw)
        except ValueError:
            return render_template(
                "result.html",
                message="Please enter a number."
            )

        message = f"You have completed {number}{goals[goal]} of {goal}."
        return render_template("result.html", message=message)

    return app

# EOF
