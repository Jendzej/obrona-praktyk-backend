import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Response, Depends, status
from jose import jwt
from sqlalchemy.exc import IntegrityError

from main import engine, models
from src.data_functions.data_delete import delete_user
from src.data_functions.data_fetch import fetch_all, fetch_user
from src.data_functions.data_insert import insert_user
from src.data_functions.data_update import update_user
from src.log import logger
from src.models import User
from src.models import example_User
from src.routers.auth import get_current_active_user

load_dotenv()

model_of_user = models[1]

router = APIRouter(
    tags=["users"]
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


@router.on_event("startup")
async def startup():
    """ Create admin on backend startup """
    username = os.getenv("PAGE_ADMIN_USERNAME")
    password = os.getenv("PAGE_ADMIN_PASSWORD")
    email = os.getenv("PAGE_ADMIN_EMAIL")
    hashed_password = jwt.encode({username: password}, SECRET_KEY, ALGORITHM)
    try:
        insert_user(engine, model_of_user, username, email, username, username, hashed_password, "admin", "1TIP")
    except IntegrityError:
        logger.info("Admin account exists, skipping")
        return


@router.get("/{user_id}")
async def get_user_by_id(user_id: int):
    """ Fetch one user by user_id """
    return fetch_user(engine, model_of_user, user_id)


@router.get("")
async def get_user(current_user: User = Depends(get_current_active_user)):
    """ Fetch current user """
    try:
        data = fetch_user(engine, model_of_user, current_user.username)
    except IntegrityError as er:
        logger.error(er)
        raise status.HTTP_422_UNPROCESSABLE_ENTITY
    return data


@router.get("/all")
async def get_all_users(current_user: User = Depends(get_current_active_user)):
    """ Fetch all users """
    if current_user.role == "admin":
        results = fetch_all(engine, model_of_user)
    else:
        raise HTTPException(
            status_code=403,
            detail="You have no permission to do that."
        )
    return results


@router.post('')
async def add_user(body: dict = example_User):
    """ Add user from POST body """
    try:
        username, email, first_name, last_name, password, school_class = body.values()
        hashed_password = jwt.encode({username: password}, SECRET_KEY, ALGORITHM)
        insert_user(engine, model_of_user, username, email, first_name, last_name, hashed_password, 'user',
                    school_class)
    except IntegrityError:
        logger.debug("Email or username is already taken")
        raise HTTPException(
            status_code=401,
            detail="Email or username is already taken"
        )
    except KeyError as er:
        logger.error(er)
        raise status.HTTP_422_UNPROCESSABLE_ENTITY

    return Response(status_code=200, content="OK")


@router.put('/{user_id}')
async def user_update(body: dict = None, current_user: User = Depends(get_current_active_user)):
    """ Update user by user_id """
    try:
        updated_user = body["updated_user"]
        if updated_user["username"] == current_user.username or current_user.role == "admin":  # TODO: username => id
            update_user(engine, model_of_user, current_user.username, updated_user)
    except KeyError as er:
        logger.error(er)
        raise status.HTTP_422_UNPROCESSABLE_ENTITY
    return Response(status_code=200, content="OK")


@router.delete("/{user_id}")
async def del_user(user_id: int, current_user: User = Depends(get_current_active_user)):
    """ Delete user by user_id """
    try:
        username = user_id  # TODO: name => id
        if username == current_user.username or current_user.role == "admin":
            delete_user(engine, model_of_user, username)
    except KeyError as er:
        logger.error(er)
        raise status.HTTP_422_UNPROCESSABLE_ENTITY
    return Response(status_code=200, content="OK")
