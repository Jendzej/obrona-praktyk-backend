import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Response, HTTPException
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
    tags=["items"]
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


class ItemEndpoints:
    def __init__(self, engine, model_of_item):
        self.engine = engine

        self.insert = Insert(self.engine)
        self.fetch = Fetch(self.engine)
        self.update = Update(self.engine)
        self.delete = Delete(self.engine)

        self.model_of_item = model_of_item

    @router.post("/add_item")
    async def add_item(self, body: dict, current_user: User = Depends(get_current_active_user)):
        item_name = body["item_name"]
        item_price = body["item_price"]
        item_description = body["item_description"]
        item_image_url = body["item_image_url"]
        try:
            self.insert.item(self.model_of_item, item_name, item_price, item_description, item_image_url)
        except IntegrityError as er:
            logger.error(er)
            raise HTTPException(
                status_code=400,
                detail=f"Integrity Error {er}"
            )
        return Response(status_code=200, content="OK")

    @router.post("/get_item")
    async def get_items(self, body: dict, current_user: User = Depends(get_current_active_user)):
        item_name = body["item_name"]
        try:
            results = self.fetch.item(self.model_of_item, item_name)
        except NoResultFound as er:
            logger.error(er)
            raise HTTPException(
                status_code=400,
                detail=f"{er}"
            )
        return results

    @router.post("/update_item")
    async def update_item(self, body: dict, current_user: User = Depends(get_current_active_user)):
        item_name = body["item_name"]
        updated_item = body["updated_item"]
        try:
            self.update.item(self.model_of_item, item_name, updated_item)
        except NoResultFound as er:
            logger.error(er)
            raise HTTPException(
                status_code=400,
                detail=f"{er}"
            )

    @router.post("/delete_item")
    async def delete_item(self, body: dict, current_user: User = Depends(get_current_active_user)):
        item_name = body["item_name"]
        try:
            self.delete.item(self.model_of_item, item_name)
        except NoResultFound as er:
            logger.error(er)
            raise HTTPException(
                status_code=400,
                detail=f"{er}"
            )
