import bcrypt
from sqlalchemy import Column, Boolean, Integer, String
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from core import app, db

class User(db.base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(32)) # TODO: this should really be a unique index
    email = Column(String(128))
    password = Column(String(64))

    def __init__(self, username='anonymous', email=None, password=None):
        self.admin = False
        self.username = username
        self.email = email
        self.password = None

        if password is not None:
            self.password = bcrypt.hashpw(password, bcrypt.gensalt())

    def __repr__(self):
        return '<User({})>'.format(self.username)

    def _encode(self):
        return {
            'id': self.id,
            'anonymous': self.id == None,
            'username': self.username,
            'email': self.email,
        }

    @classmethod
    def authenticate(cls, username, password):
        """Authenticate the given credentials, and return the user object if
        authenticated, or None if authentication failed."""

        try:
            user = db.query(User).filter(User.username == username).one()
            if bcrypt.hashpw(password, user.password) == user.password:
                return user
            else:
                return None

        except (MultipleResultsFound, NoResultFound) as e:
            return None
