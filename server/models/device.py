import uuid

import bcrypt
from sqlalchemy import (Column, Boolean, Integer, String, ForeignKey,
                        UniqueConstraint)
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from core import app, db
from models import User

class Device(db.base):
    __tablename__ = 'devices'
    __table_args__ = (
        UniqueConstraint('uid', 'name'),
    )

    id = Column(String(64), primary_key=True)
    uid = Column(Integer, ForeignKey(User.id), index=True, nullable=False)
    name = Column(String(64), nullable=False)
    serial = Column(String(250))
    push_id = Column(String(250), index=True, unique=True)
    api_key = Column(String(64), index=True, unique=True, nullable=False)

    def __init__(self, user, name):
        self.id = uuid.uuid4().hex
        self.uid = user.id
        self.name = name

        self.api_key = uuid.uuid4().hex

    def __repr__(self):
        return '<Device({},{})>'.format(self.id, self.name)

    def _encode(self):
        return {
            'id': self.id,
            'name': self.name,
            'push_id': self.push_id,
            'uri': '/api/device/' + self.id,
        }

    @classmethod
    def authenticate(cls, api_key):
        """Return a user and device object for the given api_key, if valid."""
        try:
            device = db.query(Device).filter(Device.api_key == api_key).one()
            user = User.load(device.uid)
            return user, device
        except NoResultFound as e:
            return None, None

    @classmethod
    def load(cls, did):
        """Return a device object for the given device id, or None if not found."""
        try:
            device = db.query(Device).filter(Device.id == did).one()
            return device
        except NoResultFound as e:
            return None

    @classmethod
    def load_by_user(cls, uid):
        """Returns a list of device objects for the given user id."""
        try:
            return db.query(Device).filter(Device.uid == uid).all()
        except NoResultFound:
            return []
