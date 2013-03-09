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

import logging
from logging import Formatter, FileHandler, StreamHandler
import os
from os import path
import sys

from flask import Flask

if 'APP_PATH' in os.environ:
    app_path = os.environ['APP_PATH']
else:
    app_path = path.abspath(path.dirname(path.dirname(__file__)))

app = Flask(__name__,
            static_folder=path.join(app_path, 'static'),
            template_folder=path.join(app_path, 'templates')
           )

app.config.from_pyfile(path.join(app_path, 'config.defaults'))
app.config.from_pyfile(path.join(app_path, 'config.local'), silent=True)

app.secret_key = app.config['SESSION_KEY']

formatter = Formatter('[%(asctime)s] %(levelname)s: %(message)s')
app.logger.setLevel(logging.DEBUG)
if app.config['LOG_FILE']:
    filelog = FileHandler(app.config['LOG_FILE'])
    filelog.setLevel(logging.WARNING)
    filelog.setFormatter(formatter)
    app.logger.addHandler(filelog)
if app.config['LOG_CONSOLE']:
    console = StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    app.logger.addHandler(console)
