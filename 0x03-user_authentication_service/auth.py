#!/usr/bin/env python3
"""Module for user authentication"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password as bytes.
    """
    # Encode the password to bytes
    password_bytes = password.encode('utf-8')

    # Generate a salt and hash the password
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user with email and password.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))
