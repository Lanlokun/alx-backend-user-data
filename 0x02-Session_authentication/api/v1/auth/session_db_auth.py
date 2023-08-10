#!/usr/bin/env python3
"""sessions in database module"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class.
    """

    def create_session(self, user_id=None):
        """Create session.
        """
        if user_id is None or type(user_id) is not str:
            return None
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """User ID for session ID.
        """
        if session_id is None or type(session_id) is not str:
            return None
        user_session = UserSession.search({'session_id': session_id})
        if len(user_session) == 0:
            return None
        user_session = user_session[0]
        if self.session_duration <= 0:
            return user_session.user_id
        created_at = user_session.created_at
        if created_at is None:
            return None
        expired_time = created_at + timedelta(seconds=self.session_duration)
        if expired_time < datetime.now():
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """Destroy session.
        """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_session = UserSession.search({'session_id': session_cookie})
        if len(user_session) == 0:
            return False
        user_session = user_session[0]
        user_session.remove()
        return True
