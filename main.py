import datetime
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy.ext.declarative import declarative_base

from src.database import Database

load_dotenv()
Base = declarative_base()

app = FastAPI()

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

model_of_gr_transaction = model_list[3]
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

time_tr = datetime.datetime.today()
db.add_multiple_records([
    model_of_transaction(user='JohnyTest', item='item1', payment_status='paid',
                         transaction_time=time_tr),
    model_of_transaction(user='JohnyTest', item='item2', payment_status='paid',
                         transaction_time=time_tr),
    model_of_transaction(user='JohnyTest', item='item3', payment_status='paid',
                         transaction_time=time_tr)
])
'''
# db.add_transaction(model_of_transaction, 'JohnyTest', 'item2', 'paid', datetime.datetime.today())

# db.group_transaction(model_of_transaction, model_of_gr_transaction, model_of_item, 'JohnyTest',
#                      datetime.datetime.today())

db.user_update(model_of_user, 'JohnyTest', {'username': 'JohnyFest'})


@app.post('/add_transaction')
async def add_item_to_transaction(body: dict):
    # user, items: list, payment_status
    user: str = body['user']
    items: list = body['items']
    payment_status: str = body['payment_status']
    transaction_time: datetime = datetime.datetime.today()
    for item in items:
        db.add_one_record(model_of_transaction(user=user, item=item, payment_status=payment_status,
                                               transaction_time=transaction_time))
    db.group_transaction(model_of_transaction, model_of_gr_transaction, model_of_item, user, transaction_time)
