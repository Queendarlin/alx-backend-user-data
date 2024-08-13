#!/usr/bin/env python3
"""Flask app for user authentication.
"""
from flask import Flask, jsonify, request, abort, redirect
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


@app.route('/sessions', methods=['DELETE'])
def logout():
    """Log out a user by destroying their session."""
    session_id = request.cookies.get('session_id')

    # Check if the session_id exists
    if session_id is None:
        abort(403)

    # Find the user by session_id
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    # Destroy the session and redirect to the homepage
    AUTH.destroy_session(user.id)

    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile():
    """Return user profile information based on session_id."""
    session_id = request.cookies.get('session_id')

    # Check if the session_id exists
    if session_id is None:
        abort(403)

    # Find the user by session_id
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    # Return the user's email in JSON format
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """Handle POST /reset_password request."""
    email = request.form.get('email')

    if not email:
        abort(400, description="Email is required")

    try:
        # Generate the reset token
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({
            "email": email,
            "reset_token": reset_token
        }), 200
    except ValueError:
        # Email is not registered
        abort(403, description="Email not registered")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
