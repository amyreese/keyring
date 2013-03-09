# Copyright 2013 John Reese
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

        if authenticated:
            return f(*args, **kwargs)
        abort(403)

    authenticated_methods.add(decorated_function)
    return decorated_function
