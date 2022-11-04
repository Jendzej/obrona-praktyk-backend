import datetime
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

'''
db.add_one_record(
    model_of_user(username='JohnyTest', email='email3', first_name='Johny', last_name='Test', password='password',
                  role='admin', school_class='4TIP'))
db.add_one_record(
    model_of_user(username='TommyFest', email='email2', first_name='Tommy', last_name='Fest', password='password',
                  role='admin', school_class='1TI1'))

db.add_multiple_records([
    model_of_item(item_name='item1', item_price=10, item_description='desc of item1', item_image_url='url item1'),
    model_of_item(item_name='item2', item_price=15, item_description='desc of item2', item_image_url='url item2'),
    model_of_item(item_name='item3', item_price=20, item_description='desc of item3', item_image_url='url item3'),
])
'''
# db.fetch_transactions(model_of_transaction, '')
'''
db.add_multiple_records([
    model_of_transaction(user='jedrzej1', item='item1', payment_status='paid',
                         transaction_time=datetime.datetime.today()),
    model_of_transaction(user='jedrzej1', item='item2', payment_status='paid',
                         transaction_time=datetime.datetime.today()),
    model_of_transaction(user='jedrzej1', item='item3', payment_status='paid',
                         transaction_time=datetime.datetime.today())
])
'''