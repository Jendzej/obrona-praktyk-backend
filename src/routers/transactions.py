from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Response, status, HTTPException
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


@router.get('')
async def get_transactions(current_user: User = Depends(get_current_active_user)):
    """ Fetch all transactions for current user """
    results = fetch_users_transactions(engine, model_of_transaction, username=current_user.username)
    return results


@router.post("")
async def add_transaction(body: dict, current_user: User = Depends(get_current_active_user)):
    """ Add transaction from POST body """
    try:
        items, payment_status, tr_time, del_time = body.values()
        for item in items:
            insert_transaction(engine, model_of_transaction, user=current_user.username, item=item,
                               payment_status=payment_status, transaction_time=tr_time, delivery_time=del_time)
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
        transaction_time = transaction_id  # TODO: time => id
        delete_transaction(engine, model_of_transaction, transaction_time)
        logger.debug(f"Transaction at '{transaction_time}' successfully deleted!")
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
