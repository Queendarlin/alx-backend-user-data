#!/usr/bin/env python3
"""Flask app for user authentication.
"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def index() -> jsonify:
    """Handles the GET request for the root route.

    Returns:
        jsonify: JSON response with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user() -> jsonify:
    """Handles user registration through POST request.

        Expects form data with 'email' and 'password' fields.
        Returns:
            jsonify: JSON response with success or error message.
    """
    data = request.form

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
