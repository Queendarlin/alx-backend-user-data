# Flask Session Authentication

## Description

This is a basic Flask application implementing session-based authentication. Users can register, log in, and log out. Protected routes require authentication via session cookies.

## Setup

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install dependencies (Flask is the only dependency required):
    ```bash
    pip install flask
    ```

3. Run the application:
    ```bash
    python app.py
    ```

4. Use Postman or `curl` to test the API endpoints.

## Endpoints

- `POST /register` - Register a new user.
- `POST /login` - Log in a user.
- `GET /logout` - Log out the current user.
- `GET /profile` - Access a protected profile route.

## Notes

- The `app.secret_key` should be a random, secure string in production.
