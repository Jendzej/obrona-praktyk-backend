from sqlalchemy.ext.declarative import declarative_base

from src.db import db

Base = declarative_base()
db.connecting_db()
db.init.create_tables(Base)
engine = db.engine
models = db.models
