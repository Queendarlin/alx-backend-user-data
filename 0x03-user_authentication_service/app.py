#!/usr/bin/env python3
"""Flask app for user authentication.
"""
from flask import Flask, jsonify, request, abort
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
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """Log in a user and create a new session."""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(401)  # Missing email or password

    if not AUTH.valid_login(email, password):
        abort(401)  # Invalid login credentials

    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)  # Unable to create session

    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
