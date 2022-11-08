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
    tags=["items"]
)

Base = declarative_base()
db = Database(os.getenv("POSTGRES_USER"), os.getenv("POSTGRES_PASSWORD"), os.getenv("POSTGRES_HOST"),
              os.getenv("POSTGRES_PORT"), os.getenv("POSTGRES_DB"))
db.connecting_db()

model_list = db.init.create_tables(Base)
model_of_item = model_list[0]
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


@router.post("/add_item")
async def add_item(body: dict, current_user: User = Depends(get_current_active_user)):
    item_name = body["item_name"]
    item_price = body["item_price"]
    item_description = body["item_description"]
    item_image_url = body["item_image_url"]
    try:
        db.insert.item(model_of_item, item_name, item_price, item_description, item_image_url)
    except IntegrityError as er:
        logger.error(er)
        raise