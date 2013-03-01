import os
from os import path
import sys

cwd = path.abspath(path.dirname(__file__))
sys.path.insert(0, cwd)

os.environ['APP_PATH'] = cwd

from core import app as application
import models, views

if __name__ == '__main__':
    # create database schema
    if 'schema' in sys.argv:
        print "creating database schema"

        print ">>> from core import db"
        from core import db

        print ">>> db.base.metadata.create_all()"
        db.base.metadata.create_all()

    # setup debug shell
    if 'shell' in sys.argv:
        print "debug shell"

        print ">>> from core import app, db, mc"
        from core import app, db, mc

        print ">>> from models import User, Device"
        from models import User, Device

    # run integrated debug server
    if len(sys.argv) == 1:
        application.run(host='0.0.0.0', port=8000, debug=True)
