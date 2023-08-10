#!/usr/bin/env python3
""" Module of Authentication
"""
from typing import List, TypeVar
from os import getenv


class Auth:
    """Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require auth
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'

        if path in excluded_paths:
            return False

        for excluded_path in excluded_paths:
            if excluded_path[-1] == '*':
                if path.startswith(excluded_path[:-1]):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user
        """
        return None

    def session_cookie(self, request=None):
        """Session cookie
        """
        if request is None:
            return None

        SESSION_NAME = getenv('SESSION_NAME')
        return request.cookies.get(SESSION_NAME)
