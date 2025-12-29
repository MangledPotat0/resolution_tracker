# -*- coding: utf-8 -*-
"""
interface.py
This module controls and provides the rendering of the web app that is served
to the user.
"""

# 3rd party module imports
from flask import Flask, render_template

def create_app() -> Flask:
    """
    Factory method to create the web app. The run.py entrypoint invokes this
    method once.

    Returns:
        Flask app object
    """
    app = Flask(__name__)
 
    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/options")
    def options():
        # These are options to be populated by database

        items = ["Apple", "Banana", "Pineapple"]
        return "".join(f"<option value='{i}'>{i}</option>" for i in items)

    return app

# EOF
