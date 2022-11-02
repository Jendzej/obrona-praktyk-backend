import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Sequence, Column, Integer, String, Float, ForeignKey, DateTime, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError
# from psycopg2 import errors
import time
import datetime

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

    # @connecting_db
    def create_tables(self, base):
        model_list = create_models(self.engine, base)
        return model_list

    def add_item(self, item_model, item_name, item_price, item_description, item_image_url):
        session = sessionmaker(bind=self.engine)
        sess = session()
        item_to_add = item_model(
            item_name=item_name,
            item_price=item_price,
            item_description=item_description,
            item_image_url=item_image_url
        )
        sess.add(item_to_add)
        sess.commit()
        data = sess.query(item_model).first()
        return data

    def add_school_classes(self, school_class_model, school_class):
        session = sessionmaker(bind=self.engine)
        sess = session()
        school_class_to_add = school_class_model(
            school_class=school_class
        )
        sess.add(school_class_to_add)

        try:
            sess.commit()
            data = sess.query(school_class_model).first()
        except IntegrityError as ie:
            return ie

        return data

    def add_role(self, role_model, role):
        session = sessionmaker(bind=self.engine)
        sess = session()
        role_to_add = role_model(
            role=role
        )
        sess.add(role_to_add)
        try:
            sess.commit()
            data = sess.query(role_model).first()
        except IntegrityError as ie:
            return ie

        return data

    def add_payment_status(self, payment_status_model, status):
            session = sessionmaker(bind=self.engine)
            sess = session()
            status_to_add = payment_status_model(
                status=status
            )
            sess.add(status_to_add)
            try:
                sess.commit()
                data = sess.query(payment_status_model).first()
            except IntegrityError as ie:
                return ie

            return data

    def add_user(self, user_model, username, first_name, last_name, password, role, school_class):
        session = sessionmaker(bind=self.engine)
        sess = session()
        user_to_add = user_model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role=role,
            school_class=school_class
        )
        sess.add(user_to_add)

        try:
            sess.commit()
            data = sess.query(user_model).first()
        except IntegrityError as ie:
            return ie

        return data

    def add_transaction(self, transaction_model, user, item, payment_status):
        session = sessionmaker(bind=self.engine)
        sess = session()
        transaction_to_add = transaction_model(
            user=user,
            item=item,
            payment_status=payment_status
        )
        sess.add(transaction_to_add)

        try:
            sess.commit()
            data = sess.query(transaction_model).first()
        except IntegrityError as ie:
            return ie

        return data


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

# print(models)
# print(item_model)

# print(db.add_role(roles, "admin"))
# print(db.add_school_classes(school_class_models, "4TIP"))
# print(db.add_payment_status(payment_status_model, "paid"))
# print(db.add_payment_status(payment_status_model, "not paid"))
# print(db.add_payment_status(payment_status_model, "pending"))
# print(db.add_item(item_model, "Bułka", 10.10, "Bułka smaczna, z ogórkiem", "url"))
# print(db.add_user(users_model, "jendrzej24", "Jędrzej", "Runowicz", "Haslo", "admin", "4TIP"))
print(db.add_transaction(transactions_model, "jendrzej24",  "Bułka", "paid"))
