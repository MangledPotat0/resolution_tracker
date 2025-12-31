# -*- coding: utf-8 -*-
"""
interface.py
This module controls and provides the rendering of the web app that is served
to the user.
"""
# 3rd party module imports
from flask import Flask, render_template, request

# local module imports
from app.db.connection import db_connect, db_close

def create_app() -> Flask:
    """
    Factory method to create the web app. The run.py entrypoint invokes this
    method once.

    Returns:
        Flask app object
    """
    app = Flask(__name__)
    app.db = db_connect()
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
