import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound

from main import engine, models
from src.data_functions.data_delete import delete_item
from src.data_functions.data_fetch import fetch_item, fetch_all
from src.data_functions.data_insert import insert_item
from src.data_functions.data_update import update_item
from src.log import logger
from src.models import User
from src.routers.auth import get_current_active_user

load_dotenv()

router = APIRouter(
    tags=["items"]
)
model_of_item = models[0]

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


@router.post("/add_item")
async def add_item(body: dict, current_user: User = Depends(get_current_active_user)):
    try:
        item_name = body["item_name"]
        item_price = body["item_price"]
        item_description = body["item_description"]
        item_image_url = body["item_image_url"]
        if current_user.role == "admin":
            insert_item(engine, model_of_item, item_name, item_price, item_description, item_image_url)
            return Response(status_code=200, content="OK")
        else:
            return HTTPException(
                status_code=403,
                detail="You don't have permissions to do that."
            )
    except IntegrityError as er:
        logger.error(er)
        return HTTPException(
            status_code=400, detail=f"{er}"
        )
    except KeyError as er:
        logger.error(er)
        return HTTPException(
            status_code=422, detail=f"{er}"
        )


@router.post("/get_item")
async def get_item(body: dict, current_user: User = Depends(get_current_active_user)):
    try:
        item_name = body["item_name"]
        results = fetch_item(engine, model_of_item, item_name)
        return results
    except NoResultFound as er:
        logger.error(er)
        return HTTPException(
            status_code=400, detail=f"{er}"
        )
    except KeyError as er:
        logger.error(er)
        return HTTPException(
            status_code=422, detail=f"{er}"
        )


@router.post("/get_all_items")
async def get_all_items():
    results = fetch_all(engine, model_of_item)
    if len(results) == 0:
        return HTTPException(
            status_code=200, detail="OK, Nothing to show"
        )
    return results


@router.post("/update_item")
async def item_update(body: dict, current_user: User = Depends(get_current_active_user)):
    try:
        item_name = body["item_name"]
        updated_item = body["updated_item"]
        if current_user.role == "admin":
            update_item(engine, model_of_item, item_name, updated_item)
        else:
            return HTTPException(
                status_code=403,
                detail="You don't have permission to do that."
            )
    except NoResultFound as er:
        logger.error(er)
        return HTTPException(
            status_code=400,
            detail=f"{er}"
        )
    except KeyError as er:
        logger.error(er)
        return HTTPException(
            status_code=422,
            detail=f"{er}"
        )
    return Response(status_code=200, content="OK")


@router.post("/delete_item")
async def del_item(body: dict, current_user: User = Depends(get_current_active_user)):
    try:
        item_name = body["item_name"]
        if current_user.role == "admin":
            delete_item(engine, model_of_item, item_name)
            return Response(status_code=200, content="OK")
        else:
            return HTTPException(
                status_code=403,
                detail="You have no permission to do that."
            )
    except NoResultFound as er:
        logger.error(er)
        return HTTPException(
            status_code=400,
            detail=f"{er}"
        )
    except KeyError as er:
        logger.error(er)
        return HTTPException(
            status_code=422,
            detail=f"{er}"
        )
