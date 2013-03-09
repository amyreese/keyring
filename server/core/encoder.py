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

import json

class Encoder(json.JSONEncoder):
    def default(self, o):
        try:
            return o._encode()
        except:
            return str(o)

def dump(obj, pretty=True):
    indent = None
    if pretty:
        indent = 4

    return json.dumps(obj, cls=Encoder, indent=indent)
dumps = dump

def load(s):
    return json.loads(s)

def idify(name):
    """Create an ID string from a name by replacing periods and spaces with underscores."""
    return name.replace(' ', '_').replace('.', '_').lower()
