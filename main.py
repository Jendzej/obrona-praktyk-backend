import os

from dotenv import load_dotenv
# from fastapi import FastAPI
from sqlalchemy.ext.declarative import declarative_base

from src.database import Database

load_dotenv()
Base = declarative_base()

# app = FastAPI()

db = Database(os.getenv("POSTGRES_USER"), os.getenv("POSTGRES_PASSWORD"), os.getenv("POSTGRES_HOST"),
              os.getenv("POSTGRES_PORT"), os.getenv("POSTGRES_DB"))
db.connecting_db()

model_list = db.create_tables(Base)
model_of_item = model_list[0]
# item_name='', item_price='', item_description='', item_image_url=''

model_of_user = model_list[1]
# username='', email='', first_name='', last_name='', password='',role='', school_class=''

model_of_transaction = model_list[2]
# user='', item='', payment_status='', transaction_time=datetime.datetime.today()

# print(db.user_update(model_of_user, 'janusz121', {'username': 'jedrzej123'}))
# print(db.get_user(model_of_user, 'jedrzej150'))
# db.add_one_record(
#     model_of_user(username='janusz121', email='email1', first_name='jan', last_name='Huan', password='Haslo',
#                   role='user', school_class='1TI1'))
# db.add_one_record(
#     model_of_user(username='marcin53', email='email2', first_name='Marcin', last_name='Flak', password='Haslo',
#                   role='admin', school_class='1TI2'))
# db.add_one_record(
#     model_of_user(username='kubaPunk', email='email3', first_name='Kuba', last_name='Punk', password='Haslo',
#                   role='user', school_class='1TR'))
print(db.get_table_data(model_of_user))
