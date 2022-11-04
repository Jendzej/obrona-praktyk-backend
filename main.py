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

db.add_one_record(model_of_item(item_name='Bagietka czosnkowa', item_price='3.5',
                                item_description='Bagietka upieczona z masłem ziołowo czosnkowym w środku',
                                item_image_url='url2'))
