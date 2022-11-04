import time

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.ext.declarative import declarative_base

from src.data_functions import add_data, add_multiple_data, select_user, update_user
from src.fetch_data import fetch_last, fetch_all
from src.initial_db_data import initial_insertion
from src.log import logger
from src.models import create_models

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

    def connecting_db(self):
        logger.info("Connecting to database ...")
        while True:
            try:
                self.engine.connect()
                break
            except OperationalError as OpErr:
                logger.debug(OpErr)
                logger.info("Trying again...")
                time.sleep(2)
                continue

        return logger.info("Connected")

    def create_tables(self, base):
        model_list = create_models(self.engine, base)
        model_school_classes = model_list[0][0]
        model_roles = model_list[0][1]
        model_payment_status = model_list[0][2]
        initial_models = [model_school_classes, model_roles, model_payment_status]

        try:
            initial_insertion(self.engine, initial_models)
            logger.info("Inserted database start data")
        except IntegrityError as IE:
            logger.info("Database start data already exists, skipping insertion")
        return model_list[1]

    def add_one_record(self, model):
        add_data(self.engine, model)

    def add_multiple_records(self, models: list):
        add_multiple_data(self.engine, models)

    def fetch_one_last(self, model):
        return fetch_last(self.engine, model)

    def fetch_all_data(self, model):
        return fetch_all(self.engine, model)

    def get_user(self, model, username):
        return select_user(self.engine, model, username)

    def user_update(self, user_model, username, new_user_data: dict):
        return update_user(self.engine, user_model, username, new_user_data)
