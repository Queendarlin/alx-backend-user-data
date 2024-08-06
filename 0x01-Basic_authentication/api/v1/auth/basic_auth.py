#!/usr/bin/env python3
"""Module for basic authentication"""

import re
from api.v1.auth.auth import Auth
import base64


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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str) -> str:
        """ Decodes the Base64 part of the Authorization header"""
        if base64_authorization_header is None or not\
                isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None
