import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Response, Depends
from jose import jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

from src.database import Database
from src.log import logger
from src.models import User
from src.routers.auth import get_current_active_user

load_dotenv()

router = APIRouter(
    tags=["users"]
)

Base = declarative_base()
db = Database(os.getenv("POSTGRES_USER"), os.getenv("POSTGRES_PASSWORD"), os.getenv("POSTGRES_HOST"),
              os.getenv("POSTGRES_PORT"), os.getenv("POSTGRES_DB"))
db.connecting_db()

model_list = db.init.create_tables(Base)
model_of_user = model_list[1]
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


@router.post('/add_user')
async def ad_user(body: dict):
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
        db.insert.user(model_of_user, username, email, first_name, last_name, hashed_password, role, school_class)
    except IntegrityError:
        logger.debug("Email or username is already taken")
        raise HTTPException(
            status_code=401,
            detail="Email or username is already taken"
        )
    return Response(status_code=200, content="OK")


@router.post('/udate_user')
async def update_user(body: dict, current_user: User = Depends(get_current_active_user)):
    if body["username"] == current_user.username:
        try:
            db.update.user(model_of_user, current_user.username, body)
        except KeyError as er:
            logger.error(er)
