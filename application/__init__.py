from .server import app
import os

def run_app(host="0.0.0.0", port="8000", debug=True): 
    app.run(host, port, debug) 