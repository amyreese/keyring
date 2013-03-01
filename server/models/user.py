import uuid

import bcrypt
from sqlalchemy import Column, Boolean, Integer, String
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from core import app, db

class User(db.base):
    __tablename__ = 'users'

    id = Column(String(64), primary_key=True)
    email = Column(String(128), index=True, unique=True, nullable=False)
    password = Column(String(64), nullable=False)

    def __init__(self, email=None, password=None):
        self.id = None

        if email:
            self.id = uuid.uuid4().hex

        self.email = email
        self.password = None

        if password is not None:
            self.password = bcrypt.hashpw(password, bcrypt.gensalt())

    def __repr__(self):
        return '<User({})>'.format(self.email)

    def _encode(self):
        return {
            'id': self.id,
            'anonymous': self.id == None,
            'email': self.email,
        }

    @classmethod
    def authenticate(cls, email, password):
        """Authenticate the given credentials, and return the user object if
        authenticated, or None if authentication failed."""

        try:
            user = db.query(User).filter(User.email == email).one()
            if bcrypt.hashpw(password, user.password) == user.password:
                return user
            else:
                return None

        except (MultipleResultsFound, NoResultFound) as e:
            return None

    @classmethod
    def load(cls, uid):
        """Return a user object for the given user id, or None if not found."""
        try:
            user = db.query(User).filter(User.id == uid).one()
            return user
        except (MultipleResultsFound, NoResultFound) as e:
            return None
