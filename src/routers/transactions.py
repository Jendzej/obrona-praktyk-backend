import datetime

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Response

from main import models
from src.data_functions.transaction_functions import TransactionFunction
from src.log import logger
from src.models import User, example_Transaction
from src.routers.auth import get_current_active_user

load_dotenv()

router = APIRouter(
    tags=["transactions"]
)
transaction = TransactionFunction()
model_of_transaction = models[2]


@router.get('')
async def get_transactions(current_user: User = Depends(get_current_active_user)):
    """ Fetch all transactions for current user """
    data = transaction.get_all_for_user(current_user.id)
    if data:
        return data
    else:
        return Response(status_code=400, content="Bad request, something goes wrong")


@router.post("")
async def add_transaction(body: dict = example_Transaction, current_user: User = Depends(get_current_active_user)):
    """ Add transaction from POST body """
    try:
        items_ids, payment_status, del_time = body.values()
        tr_time = datetime.datetime.now()
        delivery_time = datetime.datetime.strptime(del_time, '%Y-%m-%d %H:%M')  # JS - str(Date()) to datetime.datetime
        for item_id in items_ids:
            if transaction.insert(current_user.id, item_id, payment_status, tr_time, delivery_time):
                continue
            else:
                return Response(status_code=400, content="Something goes wrong")
        return Response(status_code=200, content="Successfully added transaction to db")
    except Exception as er:
        return Response(status_code=400, content=f"Something goes wrong, {er}")


@router.put("{transaction_id}")
async def update_transaction(body: dict, transaction_id: int, current_user: User = Depends(get_current_active_user)):
    """Update transaction with new data"""
    try:
        if current_user.role == "admin":
            if transaction.update(transaction_id, body["updated_transaction"]):
                return Response(status_code=200, content="Successfully updated transaction data")
        else:
            return Response(status_code=401, content="You have no permission to do that")
    except Exception as er:
        return Response(status_code=400, content=f"Something goes wrong, {er}")


@router.delete("{transaction_id}")
async def del_transaction(transaction_id: int, current_user: User = Depends(get_current_active_user)):
    """ Delete transaction by transaction_id """
    try:
        if current_user.role == "admin":
            if transaction.delete(transaction_id):
                return Response(status_code=200, content="Successfully deleted transaction from db")
            return Response(status_code=400, content="Something goes wrong")
        else:
            return Response(status_code=401, content="You have no permission to do that")
    except Exception as er:
        logger.error(er)
        return Response(status_code=400, content=f"Something goes wrong, {er}")
