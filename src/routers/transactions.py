import datetime
import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

from src.database import Database
from src.log import logger
from src.models import User
from src.routers.auth import get_current_active_user

load_dotenv()

router = APIRouter(
    tags=["transactions"]
)

Base = declarative_base()
db = Database(os.getenv("POSTGRES_USER"), os.getenv("POSTGRES_PASSWORD"), os.getenv("POSTGRES_HOST"),
              os.getenv("POSTGRES_PORT"), os.getenv("POSTGRES_DB"))
db.connecting_db()

model_list = db.init.create_tables(Base)

model_of_item = model_list[0]
model_of_transaction = model_list[2]
model_of_gr_transaction = model_list[3]


@router.get('/get_transactions')
async def get_transactions(current_user: User = Depends(get_current_active_user)):
    results = db.fetch.users_transactions(model_of_transaction, username=current_user.username)
    return results


@router.post("/add_transaction")
async def add_transaction(body: dict, current_user: User = Depends(get_current_active_user)):
    items = body['items']
    payment_status = body['payment_status']
    tr_time = datetime.datetime.today()
    for item in items:
        try:
            db.insert.transaction(model_of_transaction, user=current_user.username, item=item,
                                  payment_status=payment_status, transaction_time=tr_time)
        except IntegrityError as IE:
            logger.error(IE)
    try:
        db.insert.group_transaction(model_of_transaction, model_of_item, model_of_gr_transaction, current_user.username,
                                    status=payment_status)
    except IntegrityError as IE:
        logger.error(IE)
