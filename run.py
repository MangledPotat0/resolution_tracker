# -*- coding: utf-8 -*-
"""
run.py
Serves as the main entrypoint of the web app. Exposes the service to port 5000
of the Docker container it resides in.
"""

# 3rd party module imports
from app.interface import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

# EOF
