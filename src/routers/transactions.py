import datetime

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Response
from sqlalchemy.exc import IntegrityError, NoResultFound

from main import engine, models
from src.data_functions.data_delete import delete_transaction
from src.data_functions.data_fetch import fetch_users_transactions
from src.data_functions.data_insert import insert_transaction
from src.log import logger
from src.models import User
from src.routers.auth import get_current_active_user

load_dotenv()

router = APIRouter(
    tags=["transactions"]
)

model_of_transaction = models[2]


@router.get('/get_transactions')
async def get_transactions(current_user: User = Depends(get_current_active_user)):
    results = fetch_users_transactions(engine, model_of_transaction, username=current_user.username)
    return results


@router.post("/add_transaction")
async def add_transaction(body: dict, current_user: User = Depends(get_current_active_user)):
    items = body['items']
    payment_status = body['payment_status']
    tr_time = datetime.datetime.today()
    for item in items:
        try:
            insert_transaction(engine, model_of_transaction, user=current_user.username, item=item,
                               payment_status=payment_status, transaction_time=tr_time)
        except IntegrityError as IE:
            logger.error(IE)
    return Response(status_code=200, content="OK")


@router.post("/delete_transaction")
async def del_transaction(body: dict):
    transaction_time = body["transaction_time"]
    try:
        delete_transaction(engine, model_of_transaction, transaction_time)
        logger.debug(f"Transaction at '{transaction_time}' successfully deleted!")
    except NoResultFound:
        logger.error(f"No Result Found for time {transaction_time}")
    return Response(status_code=200, content="OK")
