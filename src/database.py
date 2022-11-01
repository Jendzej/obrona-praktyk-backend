import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker
import time


Base = declarative_base()


class Database:
    def __init__(self, db_user, db_password, db_host, db_port, db_name):
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name

    def connecting_db(self):
        engine = create_engine(f"postgresql://{self.db_user}:{self.db_password}\
        @{self.db_host}:{self.db_port}/{self.db_name}")
        while True:
            try:
                engine.connect()
                break
            except:
                print("Trying again ...")
                time.sleep(2)
                continue

        return engine

    @staticmethod
    def create_models(base, engine_db):
        """Creating models in db"""
        item_id_sequence = Sequence('item_id_sequence')
        user_id_sequence = Sequence('user_id_sequence')

        class Items(base):
            __tablename__ = "items"
            id = Column(Integer, item_id_sequence, primary_key=True, server_default=item_id_sequence.next_value())
            item_name = Column(String(60))
            item_price = Column(Float)
            item_description = Column(String(300))
            item_image_url = Column(String(200))

            def __repr__(self):
                """Creating columns in table"""
                return f"<Items(id={self.id}, item_name={self.item_name}, item_price={self.item_price},\
                item_description={self.item_description}, item_image_url={self.item_image_url})>"

        class SchoolClasses(base):
            __tablename__ = "school_classes"
            school_class = Column(String(6), primary_key=True)

            def __repr__(self):
                """Creating column in table"""
                return f"<SchoolClasses(school_class={self.school_class})>"

        class Roles(base):
            __tablename__ = "roles"
            role = Column(String(10), primary_key=True)

            def __repr__(self):
                """Creating column in table"""
                return f"<Roles(role={self.role})>"

        class Users(base):
            __tablename__ = "users"
            id = Column(Integer, user_id_sequence, primary_key=True, server_default=user_id_sequence.next_value())
            username = Column(String(20))
            password = Column(String(30))
            role = Column(String, ForeignKey('roles.role'))
            school_class = Column(String, ForeignKey('school_classes.school_class'))

            def __repr__(self):
                return f"<Users(id={self.id}, username={self.username}, password={self.password},\
                       role={self.role}, school_class={self.school_class})>"

        base.metadata.create_all(engine_db)
        return [Items, SchoolClasses, Roles, Users]

    @staticmethod
    def add_item(engine_db, id, item_name, item_price, item_description, item_image_url):
        session = sessionmaker(bind=engine_db)


load_dotenv()

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
name = os.getenv("POSTGRES_DB")

db = Database(user, password, host, port, name)
engine = db.connecting_db()

models = db.create_models(Base, engine)

item_model = models[0]
school_class_model = models[1]
roles = models[2]
users_model = models[3]

print(models)
print(item_model)
