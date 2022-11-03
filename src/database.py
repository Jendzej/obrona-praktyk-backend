import time

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.ext.declarative import declarative_base

from fetch_data import fetch_last, fetch_all
from initial_db_data import initial_insertion
from insert_data import add_data, add_multiple_data
from models import create_models

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
        while True:
            try:
                self.engine.connect()
                break
            except OperationalError as OpErr:
                print("Trying again ...")
                print(OpErr)
                time.sleep(2)
                continue

        return "Connected!"

    def create_tables(self, base):
        model_list = create_models(self.engine, base)
        model_school_classes = model_list[0][0]
        model_roles = model_list[0][1]
        model_payment_status = model_list[0][2]
        initial_models = [model_school_classes, model_roles, model_payment_status]

        try:
            initial_insertion(self.engine, initial_models)
            print("Inserted databases initial data")
        except IntegrityError:
            print("Databases initial data already exists, skipping initialization")
        return model_list[1]

    def add_one_record(self, model):
        add_data(self.engine, model)

    def add_multiple_records(self, models: list):
        add_multiple_data(self.engine, models)

    def fetch_one_last(self, model):
        return fetch_last(self.engine, model)

    def fetch_all_data(self, model):
        return fetch_all(self.engine, model)
