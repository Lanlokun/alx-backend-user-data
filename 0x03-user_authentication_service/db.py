#!/usr/bin/env python3
"""DB module"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Save a user to the database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()

        return user
    
    def find_user_by(self, **kwargs) -> User:
        """Takes in arbitrary keyword arguments and returns the first row
        found in the users table as filtered by the method’s input arguments
        """
        if not kwargs:
            raise ValueError
        
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise ValueError
        
        return user    
    
    def update_user(self, user_id: int, **kwargs) -> None:
        """Locates the user to update, then will update the user’s attributes
        as passed in the method’s arguments then commit changes to the database
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            setattr(user, key, value)
        self._session.commit()
