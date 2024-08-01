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
