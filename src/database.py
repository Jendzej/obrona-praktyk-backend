"""Database class - engine, models and functions declaration"""
import time

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base

from src.log import logger
from src.models import create_models

Base = declarative_base()


class Database:
    """Database class"""

    def __init__(self, db_user, db_password, db_host, db_port, db_name):
        self.engine = create_engine(
            f"postgresql://{db_user}:{db_password}\@{db_host}:{db_port}/{db_name}",
            pool_size=50,
            max_overflow=20)
        self.base = declarative_base()
        self.models = create_models(self.engine, self.base)

    def connecting_db(self):
        """Connecting to database function"""
        logger.info("Connecting to database ...")
        while True:
            try:
                self.engine.connect()
                break
            except OperationalError as op_err:
                logger.error(op_err)
                logger.info("Trying again...")
                time.sleep(2)
                continue

        return logger.info("Connected")
