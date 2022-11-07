import time

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base

from src.data_functions.data_delete import Delete
from src.data_functions.data_fetch import Fetch
from src.data_functions.data_init import Init
from src.data_functions.data_insert import Insert
from src.data_functions.data_update import Update
from src.log import logger

Base = declarative_base()


def engine(db_user, db_password, db_host, db_port, db_name):
    return create_engine(f"postgresql://{db_user}:{db_password}\@{db_host}:{db_port}/{db_name}")


class Database:
    def __init__(self, db_user, db_password, db_host, db_port, db_name):
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.engine = engine(db_user, db_password, db_host, db_port, db_name)
        self.init = Init(self.engine)
        self.update = Update(self.engine)
        self.insert = Insert(self.engine)
        self.fetch = Fetch(self.engine)
        self.delete = Delete(self.engine)

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
