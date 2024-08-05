#!/usr/bin/env python3
"""Module for basic authentication"""

import re
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """class for basic authentication that inherits from Auth class"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extracts the Base64 part of the Authorization header"""
        if isinstance(authorization_header, str):
            pattern = r'Basic (?P<token>.+)'
            field_match = re.fullmatch(pattern, authorization_header.strip())
            if field_match is not None:
                return field_match.group('token')
        return None
