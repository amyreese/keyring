from functools import wraps
import re

from flask import abort, g, make_response, render_template, request

from core import app, sessions
from models import User, Device

api_key_re = re.compile(r'^api_key=([a-f0-9]+)$')
authenticated_methods = set()

def authenticate(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        authenticated = False

        if g.user.id is not None:
            authenticated = True

        elif request.authorization is not None:
            user = User.authenticate(request.authorization['username'],
                                     request.authorization['password'])
            if user is not None:
                g.user = user
                authenticated=True

        elif 'authorization' in request.headers:
            match = api_key_re.match(request.headers['authorization'])
            if match:
                user, device = Device.authenticate(match.group(1))
                if user is not None:
                    g.user = user
                    g.device = device
                    authenticated = True

            app.logger.debug('authorization: "%s"',
                             request.headers['authorization'])

        if authenticated:
            return f(*args, **kwargs)
        abort(403)

    authenticated_methods.add(decorated_function)
    return decorated_function
