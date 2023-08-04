#!/usr/bin/env python3
"""encrypting passwords"""

import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password, which is a byte string"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if a password is valid"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
