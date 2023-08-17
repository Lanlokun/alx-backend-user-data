#!/usr/bin/env python3
""" Hash password """

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ Return a salted, hashed password, which is a byte string """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Check if password is valid """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register a user """
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)
        
    def valid_login(self, email: str, password: str) -> bool:
        """ Check if login is valid """
        try:
            user = self._db.find_user_by(email=email)
            return is_valid(user.hashed_password, password)
        except NoResultFound:
            return False

    