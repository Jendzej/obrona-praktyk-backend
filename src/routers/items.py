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
from src.models import example_Item
from src.routers.auth import get_current_active_user

load_dotenv()

router = APIRouter(
    tags=["items"]
)
model_of_item = models[0]

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


@router.get("/{item_id}")
async def get_item(item_id: int, current_user: User = Depends(get_current_active_user)):
    """ Fetch one item by item_id """
    try:
        item_name = item_id  # TODO: name => id
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


@router.get("")
async def get_all_items():
    """ Fetch all items """
    results = fetch_all(engine, model_of_item)
    if len(results) == 0:
        return HTTPException(
            status_code=200, detail="OK, Nothing to show"
        )
    return results


@router.post("")
async def add_item(body: dict = example_Item, current_user: User = Depends(get_current_active_user)):
    """ Add item from POST body """
    try:
        item_name, item_price, item_description, item_image_url = body.values()
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


@router.put("/{item_id}")
async def item_update(item_id: int, body: dict, current_user: User = Depends(get_current_active_user)):
    """ Update item by item_id """
    try:
        item_name, updated_item = body.values()  # TODO: name => id
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


@router.delete("/{item_id}")
async def del_item(item_id: int, current_user: User = Depends(get_current_active_user)):
    """ Delete item by item_id """
    try:
        item_name = item_id
        if current_user.role == "admin":
            delete_item(engine, model_of_item, item_name)  # TODO: name => id
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
