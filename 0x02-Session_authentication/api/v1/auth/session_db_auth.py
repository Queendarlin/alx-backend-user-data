#!/usr/bin/env python3
""" Module for database session authentication"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class to manage session authentication with database
    """
    def create_session(self, user_id=None):
        """
        Creates and stores new instance of UserSession
        and returns the Session ID
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
          Returns the User ID
          by requesting UserSession in the database based on session_id
        """
        if session_id is None:
            return None

        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return None

        return user_sessions[0].user_id

    def destroy_session(self, request=None):
        """
        Destroys the UserSession based on the Session ID
        from the request cookie
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return False

        user_sessions[0].remove()
        return True
