#!/usr/bin/env python3
""" Module for Session authentication class"""

from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ Class for session authentication"""
    user_id_by_session_id = {}
