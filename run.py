# -*- coding: utf-8 -*-
"""
run.py
Serves as the main entrypoint of the web app. Exposes the service to port 5000
of the Docker container it resides in.
"""

# built-in module imports
import os

# 3rd party module imports
from app.interface import create_app

if __name__ == "__main__":
    app = create_app()
    service_port = int(os.getenv("SERVICE_PORT", "5000"))
    app.run(host="0.0.0.0", port=service_port, debug=True)

# EOF
