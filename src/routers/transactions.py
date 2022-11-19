import datetime

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound

from main import engine, models
from src.data_functions.data_delete import delete_transaction
from src.data_functions.data_fetch import fetch_users_transactions
from src.data_functions.data_insert import insert_transaction
from src.log import logger
from src.models import User, example_Transaction
from src.routers.auth import get_current_active_user

load_dotenv()

router = APIRouter(
    tags=["transactions"]
)

model_of_transaction = models[2]


@router.get('')
async def get_transactions(current_user: User = Depends(get_current_active_user)):
    """ Fetch all transactions for current user """
    results = fetch_users_transactions(engine, model_of_transaction, user_id=current_user.id)
    return results


@router.post("")
async def add_transaction(body: dict = example_Transaction, current_user: User = Depends(get_current_active_user)):
    """ Add transaction from POST body """
    try:
        items_ids, payment_status, del_time = body.values()
        tr_time = datetime.datetime.now()
        delivery_time = datetime.datetime.strptime(del_time, '%Y-%m-%d %H:%M')  # JS - str(Date()) to datetime.datetime
        for item_id in items_ids:
            insert_transaction(engine, model_of_transaction, user_id=current_user.id, item_id=item_id,
                               payment_status=payment_status, transaction_time=tr_time, delivery_time=delivery_time)
    except IntegrityError as IE:
        logger.error(IE)
        raise status.HTTP_422_UNPROCESSABLE_ENTITY
    except KeyError as er:
        logger.error(er)
        raise status.HTTP_422_UNPROCESSABLE_ENTITY
    return Response(status_code=200, content="OK")


@router.delete("{transaction_id}")
async def del_transaction(transaction_id: int):
    """ Delete transaction by transaction_id """
    try:
        delete_transaction(engine, model_of_transaction, transaction_id)
    except NoResultFound:
        logger.error(f"No Result Found for that time.")
        raise HTTPException(
            status_code=400,
            detail="Bad request, cannot find data."
        )
    except KeyError as er:
        logger.error(er)
        raise status.HTTP_422_UNPROCESSABLE_ENTITY
    return Response(status_code=200, content="OK")
