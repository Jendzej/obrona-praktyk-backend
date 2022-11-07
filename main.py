import datetime
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy.ext.declarative import declarative_base

from src.database import Database

load_dotenv()
Base = declarative_base()

app = FastAPI()

# CONNECTING TO DB
db = Database(os.getenv("POSTGRES_USER"), os.getenv("POSTGRES_PASSWORD"), os.getenv("POSTGRES_HOST"),
              os.getenv("POSTGRES_PORT"), os.getenv("POSTGRES_DB"))
db.connecting_db()

# MODELS
model_list = db.init.create_tables(Base)

model_of_item = model_list[0]
model_of_user = model_list[1]
model_of_transaction = model_list[2]
model_of_gr_transaction = model_list[3]

db.delete.item(model_of_item, 'item1')
db.delete.user(model_of_user, 'user1')


@app.post('/add_transaction')
async def add_item_to_transaction(body: dict):
    # user, items: list, payment_status
    user: str = body['user']
    items: list = body['items']
    payment_status: str = body['payment_status']
    transaction_time: datetime = datetime.datetime.today()
    for item in items:
        db.insert.transaction(model_of_transaction(user=user, item=item, payment_status=payment_status,
                                                   transaction_time=transaction_time))
    db.insert.group_transaction(model_of_transaction, model_of_gr_transaction, model_of_item, user, transaction_time)
