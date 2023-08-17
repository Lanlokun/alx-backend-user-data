#!/usr/bin/env python3
""" Hash password """

import bcrypt


def hash_password(password: str) -> bytes:
    """ Return a salted, hashed password, which is a byte string """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
