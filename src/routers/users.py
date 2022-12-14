import os
import time

from dotenv import load_dotenv
from fastapi import APIRouter, Response, Depends
from jose import jwt

from main import models
from src.data_functions.user import UserFunction
from src.log import logger
from src.models import User
from src.models import example_User
from src.routers.auth import get_current_active_user

load_dotenv()

model_of_user = models[1]
user = UserFunction()

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

    for i in range(3):
        if user.insert(username, email, username, username, hashed_password, "admin", "1TIP", True):
            logger.info(f"Successfully added startup user '{username}'!")
            break
        time.sleep(0.3)


@router.get("/{user_id}")
async def fetch_user_by_id(user_id: int):
    """ Fetch one user by user_id """
    return user.get(user_id)


@router.get("/")
async def fetch_user_current(current_user: User = Depends(get_current_active_user)):
    """ Fetch current user """
    return user.get(current_user.id)


@router.get("/all/")
async def fetch_all_users(current_user: User = Depends(get_current_active_user)):
    """ Fetch all users """
    if current_user.role == "admin":
        return user.get_all()
    else:
        return Response(status_code=401, content="You have no access to this data")


@router.post('/')
async def add_user(body: dict = example_User):
    """ Add user from POST body """
    username, email, first_name, last_name, password, school_class = body.values()
    hashed_password = jwt.encode({username: password}, SECRET_KEY, ALGORITHM)
    if user.insert(username, email, first_name, last_name, hashed_password, 'user',
                   school_class):
        return Response(status_code=200, content="OK")
    else:
        return Response(status_code=422, content="Can not add user...")


@router.put('/{user_id}')
async def user_update(body: dict = None, user_id: int = None, current_user: User = Depends(get_current_active_user)):
    """ Update user by user_id """
    if current_user.role == "admin" or current_user.id == user_id:
        if user.update(user_id, body["updated_user"]):
            return Response(status_code=200, content="OK")
    return Response(status_code=422, content="Can not update user...")


@router.delete("/{user_id}")
async def del_user(user_id: int, current_user: User = Depends(get_current_active_user)):
    """ Delete user by user_id """
    if user.delete(user_id):
        return Response(status_code=200, content="OK")
    else:
        return Response(status_code=422, content="Can not delete user")
