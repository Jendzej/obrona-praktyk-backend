import os
import time

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from fetch_data import fetch_last, fetch_all
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
        # engine = create_engine(f"postgresql://{self.db_user}:{self.db_password}\
        # @{self.db_host}:{self.db_port}/{self.db_name}")
        while True:
            try:
                self.engine.connect()
                break
            except:
                print("Trying again ...")
                time.sleep(2)
                continue

        return "Connected!"

    def create_tables(self, base):
        model_list = create_models(self.engine, base)
        model_school_classes = model_list[0]
        model_roles = model_list[1]
        model_payment_status = model_list[2]
        initial_models = [model_school_classes, model_roles, model_payment_status]

        return model_list

    def add_data(self, model):
        session = sessionmaker(bind=self.engine)
        sess = session()
        sess.add(model)
        sess.commit()

    def add_multiple_data(self, models: list):
        session = sessionmaker(bind=self.engine)
        sess = session()

        for model in models:
            sess.add(model)

        sess.commit()

    def fetch_one_last(self, model):
        return fetch_last(self.engine, model)

    def fetch_all_data(self, model):
        return fetch_all(self.engine, model)


load_dotenv()

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
name = os.getenv("POSTGRES_DB")

db = Database(user, password, host, port, name)
db.connecting_db()

models = db.create_tables(Base)

item_model = models[0]
school_class_models = models[1]
roles = models[2]
users_model = models[3]
transactions_model = models[4]
payment_status_model = models[5]

print(db.fetch_all_data(transactions_model))
print(db.fetch_all_data(item_model))
