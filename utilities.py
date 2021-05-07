from flask import jsonify, request
from app import app

# this is a terrible proof of concept example, obviously these would be unique to users 
# and stored in / loaded from a database 

API_TOKEN = app.config.get("API_TOKEN")

def authenticated(f):
    def wrap(*args, **kwargs):
        token = request.args.get("app-token")
        if token != API_TOKEN:
            return jsonify({"results": "failure", "message": "It's a low, low bar, and you couldn't even hit it."}), 401
        return f(*args, **kwargs)
    return wrap
