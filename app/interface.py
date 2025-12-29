# -*- coding: utf-8 -*-
# interface.py

# 3rd party module imports
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return "Hello, World!"

    return app

# EOF
