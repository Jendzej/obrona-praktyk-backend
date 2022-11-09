import datetime

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Response
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.data_functions.data_delete import Delete
from src.data_functions.data_fetch import Fetch
from src.data_functions.data_insert import Insert
from src.data_functions.data_update import Update
from src.log import logger
from src.models import User
from src.routers.auth import get_current_active_user

load_dotenv()

router = APIRouter(
    tags=["transactions"]
)


class TransactionEndpoints:
    def __init__(self, engine, model_of_item, model_of_transaction, model_of_gr_transaction):
        self.engine = engine
        self.insert = Insert(self.engine)
        self.fetch = Fetch(self.engine)
        self.update = Update(self.engine)
        self.delete = Delete(self.engine)
        self.model_of_transaction = model_of_transaction
        self.model_of_item = model_of_item
        self.model_of_gr_transaction = model_of_gr_transaction

    @router.get('/get_transactions')
    async def get_transactions(self, current_user: User = Depends(get_current_active_user)):
        results = self.fetch.users_transactions(self.model_of_transaction, username=current_user.username)
        return results

    @router.post("/add_transaction")
    async def add_transaction(self, body: dict, current_user: User = Depends(get_current_active_user)):
        items = body['items']
        payment_status = body['payment_status']
        tr_time = datetime.datetime.today()
        for item in items:
            try:
                self.insert.transaction(self.model_of_transaction, user=current_user.username, item=item,
                                        payment_status=payment_status, transaction_time=tr_time)
            except IntegrityError as IE:
                logger.error(IE)
        try:
            self.insert.group_transaction(self.model_of_transaction, self.model_of_item, self.model_of_gr_transaction,
                                          current_user.username,
                                          status=payment_status)
        except IntegrityError as IE:
            logger.error(IE)
        return Response(status_code=200, content="OK")

    @router.post("/delete_transaction")
    async def delete_transaction(self, body: dict):
        transaction_time = body["transaction_time"]
        try:
            self.delete.transaction(self.model_of_transaction, transaction_time)
            logger.debug(f"Transaction at '{transaction_time}' successfully deleted!")
        except NoResultFound:
            logger.error(f"No Result Found for time {transaction_time}")
        return Response(status_code=200, content="OK")
