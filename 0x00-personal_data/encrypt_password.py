#!/usr/bin/env python3
"""
Module for encrypting password
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
        Hashes a password with a randomly-generated salt and
        returns the hashed password.

        Args:
            password (str): The password to hash.

        Returns:
            bytes: The salted and hashed password.
        """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
        Validates that the provided password matches the hashed password.

        Args:
            hashed_password (bytes): The hashed password to check against.
            password (str): The plain text password to validate.

        Returns:
            bool: True if the password matches the hashed password,
            False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
