from flask import flash, g, redirect, request

from core import app, db, sessions, api, context, get, post, template
from models import Device

@api('/devices', methods=['GET'])
def api_device_list(method):
    if g.user.id is None:
        return []
    else:
        return Device.load_by_user(g.user.id)

with context('/device'):
    pass

