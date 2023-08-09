#!/usr/bin/env python3
"""Basic authentication module."""


from api.v1.auth.auth import Auth
from base64 import b64decode


class BasicAuth(Auth):
    """BasicAuth class.
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract base64 authorization header.
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if authorization_header[:6] != 'Basic ':
            return None
        return authorization_header[6:]
