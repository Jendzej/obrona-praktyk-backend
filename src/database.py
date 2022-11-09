import time

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base

from src.data_functions.data_init import Init
from src.log import logger

Base = declarative_base()


def engine(db_user, db_password, db_host, db_port, db_name):
    return create_engine(f"postgresql://{db_user}:{db_password}\@{db_host}:{db_port}/{db_name}", pool_size=50,
                         max_overflow=20)


class Database:
    def __init__(self, db_user, db_password, db_host, db_port, db_name):

        print("src/datatabase init")
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.engine = engine(db_user, db_password, db_host, db_port, db_name)
        self.init = Init(self.engine)
        self.base = declarative_base()
        self.models = self.init.create_tables(self.base)

    def connecting_db(self):
        logger.info("Connecting to database ...")
        while True:
            try:
                self.engine.connect()
                break
            except OperationalError as OpErr:
                logger.error(OpErr)
                logger.info("Trying again...")
                time.sleep(2)
                continue

        return logger.info("Connected")

    # def get_models(self):
