import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Response, Depends, status
from jose import jwt
from sqlalchemy.exc import IntegrityError

from main import engine, models
from src.data_functions.data_delete import delete_user
from src.data_functions.data_fetch import fetch_all, fetch_user
from src.data_functions.data_insert import insert_user
from src.log import logger
from src.models import User
from src.routers.auth import get_current_active_user

load_dotenv()

model_of_user = models[1]

router = APIRouter(
    tags=["users"]
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


@router.post('/add_user')
async def add_user(body: dict = None):
    """Endpoint for adding users"""
    username = body['username']
    email = body['email']
    first_name = body['first_name']
    last_name = body['last_name']
    password = body['password']
    role = 'user'
    school_class = body['school_class']

    hashed_password = jwt.encode({username: password}, SECRET_KEY, ALGORITHM)
    try:
        insert_user(engine, model_of_user, username, email, first_name, last_name, hashed_password, role, school_class)
    except IntegrityError:
        logger.debug("Email or username is already taken")
        raise HTTPException(
            status_code=401,
            detail="Email or username is already taken"
        )
    return Response(status_code=200, content="OK")


@router.get("/get_user")
async def get_user(current_user: User = Depends(get_current_active_user)):
    try:
        data = fetch_user(engine, model_of_user, current_user.username)
    except IntegrityError as er:
        logger.error(er)
        raise status.HTTP_422_UNPROCESSABLE_ENTITY
    return data


@router.get("/get_all_users")
async def get_all_users(current_user: User = Depends(get_current_active_user)):
    if current_user.role == "admin":
        results = fetch_all(engine, model_of_user)
    else:
        raise HTTPException(
            status_code=403,
            detail="You have no permission to do that."
        )
    return results


@router.post('/update_user')
async def update_user(body: dict = None, current_user: User = Depends(get_current_active_user)):
    updated_user = body["updated_user"]
    if updated_user["username"] == current_user.username or current_user.role == "admin":
        try:
            updated_user(engine, model_of_user, current_user.username, updated_user)
        except KeyError as er:
            logger.error(er)
            raise status.HTTP_422_UNPROCESSABLE_ENTITY
    return Response(status_code=200, content="OK")


@router.post("/delete_user")
async def del_user(body: dict = None, current_user: User = Depends(get_current_active_user)):
    username = body["username"]
    if username == current_user.username or current_user.role == "admin":
        try:
            delete_user(engine, model_of_user, username)
        except KeyError as er:
            logger.error(er)
            raise status.HTTP_422_UNPROCESSABLE_ENTITY
    return Response(status_code=200, content="OK")
