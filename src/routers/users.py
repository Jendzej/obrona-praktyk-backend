import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Response, Depends, status
from jose import jwt
from sqlalchemy.exc import IntegrityError

from main import engine, models
from src.data_functions.data_fetch import fetch_user_by_id, fetch_all
from src.data_functions.users_functions import UserFunction
from src.log import logger
from src.models import User
from src.models import example_User
from src.routers.auth import get_current_active_user, create_access_token

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
    try:
        user.insert(username, email, username, username, hashed_password, "admin", "1TIP", True)
    except Exception as er:
        logger.info("Db contains admin account already")


@router.get("/{user_id}")
async def get_user_by_id(user_id: int):
    """ Fetch one user by user_id """
    return fetch_user_by_id(engine, model_of_user, user_id)


@router.get("/")
async def get_user_current(current_user: User = Depends(get_current_active_user)):
    """ Fetch current user """
    try:
        data = fetch_user_by_id(engine, model_of_user, current_user.id)
    except IntegrityError as er:
        logger.error(er)
        raise status.HTTP_422_UNPROCESSABLE_ENTITY
    return data


@router.get("/all")
async def get_all_users(current_user: User = Depends(get_current_active_user)):
    """ Fetch all users """
    print("GETTING")
    if current_user.id == 1:
        # results = user.get_all()
        results = fetch_all(engine, model_of_user)
    else:
        raise HTTPException(
            status_code=403,
            detail="You have no permission to do that."
        )
    return results


@router.post('/')
async def add_user(body: dict = example_User):
    """ Add user from POST body """
    username, email, first_name, last_name, password, school_class = body.values()
    if user.insert(username, email, first_name, last_name, create_access_token({username: password}), 'user',
                   school_class):
        return Response(status_code=200, content="OK")
    else:
        return Response(status_code=422, content="Can not add user...")


@router.put('/{user_id}')
async def user_update(body: dict = None, user_id: int = None, current_user: User = Depends(get_current_active_user)):
    """ Update user by user_id """
    if user.update(user_id, body["updated_user"]):
        return Response(status_code=200, content="OK")
    else:
        return Response(status_code=422, content="Can not update user...")


@router.delete("/{user_id}")
async def del_user(user_id: int, current_user: User = Depends(get_current_active_user)):
    """ Delete user by user_id """
    print(current_user)
    if user.delete(user_id):
        return Response(status_code=200, content="OK")
    else:
        return Response(status_code=422, content="Can not delete user")
