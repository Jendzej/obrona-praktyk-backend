import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence, Column, Integer, String, Float, ForeignKey, DateTime, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError
from psycopg2 import errors
import time
import datetime

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

    # def create_models(self, base):
    #     """Creating models in db"""
    #     item_id_sequence = Sequence('item_id_sequence')
    #     transaction_sequence = Sequence('transaction_sequence')
    #
    #     class Items(base):
    #         __tablename__ = "items"
    #         id = Column(Integer, item_id_sequence, primary_key=True, server_default=item_id_sequence.next_value())
    #         item_name = Column(String(60), unique=True)
    #         item_price = Column(Float)
    #         item_description = Column(String(300))
    #         item_image_url = Column(String(200))
    #
    #         def __repr__(self):
    #             """Creating columns in table"""
    #             return f"<Items(id={self.id}, item_name={self.item_name}, item_price={self.item_price}, item_description={self.item_description}, item_image_url={self.item_image_url})>"
    #
    #     class SchoolClasses(base):
    #         __tablename__ = "school_classes"
    #         school_class = Column(String(6), primary_key=True)
    #
    #         def __repr__(self):
    #             """Creating column in table"""
    #             return f"<SchoolClasses(school_class={self.school_class})>"
    #
    #     class Roles(base):
    #         __tablename__ = "roles"
    #         role = Column(String(10), primary_key=True)
    #
    #         def __repr__(self):
    #             """Creating column in table"""
    #             return f"<Roles(role={self.role})>"
    #
    #     class PaymentStatus(base):
    #         __tablename__ = "payment_status"
    #         status = Column(String(15), primary_key=True, unique=True)
    #
    #         def __repr__(self):
    #             """Creating column in table"""
    #             return f"<PaymentStatus(role={self.role})>"
    #
    #     class Users(base):
    #         __tablename__ = "users"
    #         username = Column(String(20), primary_key=True)
    #         first_name = Column(String(30))
    #         last_name = Column(String(30))
    #         password = Column(String(30))
    #         role = Column(String, ForeignKey('roles.role'))
    #         school_class = Column(String, ForeignKey('school_classes.school_class'))
    #         transaction_item = relationship('Items', secondary='transactions', backref='transaction_items')
    #
    #         def __repr__(self):
    #             return f"<Users(username={self.username}, first_name={self.first_name}, last_name={self.last_name}, password={self.password}, role={self.role}, school_class={self.school_class})>"
    #
    #     class Transactions(base):
    #         user = Column(String, ForeignKey("users.username"))
    #         item = Column(String, ForeignKey("items.item_name"))
    #         payment_status = Column(String, ForeignKey("payment_status.status"))
    #
    #         def __repr__(self):
    #             return f"<Transactions(user={self.user}, item={self.item}, payment_status={self.payment_status})>"
    #
    #     # class Transactions(base):
    #     #     __tablename__ = "transactions"
    #     #     id = Column(Integer, transaction_sequence, primary_key=True, server_default=transaction_sequence.next_value())
    #     #     user = Column(String, ForeignKey('users.username'))
    #     #     value = Column(Integer)
    #     #     items = Column(String, ForeignKey("items.item_name"))
    #     #     transaction_time = Column(DateTime)
    #     #
    #     #     def __repr__(self):
    #     #         return f"<Transactions(id={self.id}, user={self.user}, value={self.value}, items={self.items}, transaction_time={self.transaction_time})>"
    #
    #     base.metadata.create_all(self.engine)
    #     return [Items, SchoolClasses, Roles, Users, Transactions, PaymentStatus]

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

    def add_transaction(self, transaction_model, user, value, items, transaction_time):
        session = sessionmaker(bind=self.engine)
        sess = session()
        transaction_to_add = transaction_model(
            user=user,
            value=value,
            items=items,
            transaction_time=transaction_time
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

models = db.create_models(Base)

item_model = models[0]
school_class_models = models[1]
roles = models[2]
users_model = models[3]
transactions_model = models[4]

# print(models)
# print(item_model)

# print(db.add_item(item_model, "Przedmiot 6", 15.15, "Super przedmiot12, polecam", "url2s"))
# print(db.add_user(users_model, "jendrzej24", "Jędrzej", "Runowicz", "Haslo", "admin", "4TIP"))
# print(db.add_school_classes(school_class_models, "4TIP"))
# print(db.add_role(roles, "admin"))
print(db.add_transaction(transactions_model, "jendrzej24", 13.43, "Przedmiot), (Przedmiot 6", datetime.date.today()))
