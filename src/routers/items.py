import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Response

from main import startup_items
from src.data_functions.items_functions import ItemFunction
from src.log import logger
from src.models import User
from src.models import example_Item
from src.routers.auth import get_current_active_user

load_dotenv()

router = APIRouter(
    tags=["items"]
)
item = ItemFunction()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


@router.on_event("startup")
async def startup():
    for single_item in startup_items:
        name, price, description, url = single_item
        if item.insert(name, price, description, url, True):
            logger.debug(f"Successfully added item '{name}' to items!")
 

@router.get("/{item_id}")
async def fetch_item(item_id: int, current_user: User = Depends(get_current_active_user)):
    """ Fetch one item by item_id """
    return item.get(item_id)


@router.get("/all/")
async def fetch_all_items():
    """ Fetch all items """
    return item.get_all()


@router.post("")
async def add_item(body: dict = example_Item, current_user: User = Depends(get_current_active_user)):
    """ Add item from POST body """
    try:
        item_name, item_price, item_description, item_image_url = body.values()
        if current_user.role == "admin":
            if item.insert(item_name, item_price, item_description, item_image_url):
                return Response(status_code=200, content=f"Successfully added item {item_name}")
            else:
                return Response(status_code=404, content="Bad request, item was not added")
        else:
            return Response(status_code=401, content="You have no permissions to do that!")
    except Exception as er:
        return Response(status_code=422, content=f"Unprocessable entity, {er}")


@router.put("/{item_id}")
async def item_update(item_id: int, body: dict, current_user: User = Depends(get_current_active_user)):
    """ Update item by item_id """
    try:
        if current_user.role == "admin":
            if item.update(item_id, body["updated_item"]):
                return Response(status_code=200, content=f"Successfully updated item with id {item_id}")
            else:
                return Response(status_code=404, content="Bad request, item was not added")
        else:
            return Response(status_code=401, content=f"You have no permissions to do that!")
    except Exception as er:
        print(er)
        return Response(status_code=422, content=f"Something went wrong..., {er}")


@router.delete("/{item_id}")
async def del_item(item_id: int, current_user: User = Depends(get_current_active_user)):
    """ Delete item by item_id """
    if current_user.role == "admin":
        if item.delete(item_id):
            return Response(status_code=200, content=f"Successfully deleted item with id {item_id}")
        else:
            return Response(status_code=400, content="Item does not exists or something goes wrong")
    else:
        return Response(status_code=401, content="You have no access to do that!")
