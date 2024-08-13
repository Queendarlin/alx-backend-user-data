#!/usr/bin/env python3
"""Flask app for user authentication.
"""
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index() -> jsonify:
    """Handles the GET request for the root route.

    Returns:
        jsonify: JSON response with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
