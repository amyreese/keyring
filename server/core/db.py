import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core import app

engine = sqlalchemy.create_engine(app.config['DB_URI'])

base = declarative_base(bind=engine)
transaction = sessionmaker(bind=engine)
db = transaction(expire_on_commit=False)
db.base = base
