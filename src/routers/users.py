import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Response, Depends
from jose import jwt
from sqlalchemy.exc import IntegrityError

from src.data_functions.data_delete import Delete
from src.data_functions.data_fetch import Fetch
from src.data_functions.data_insert import Insert
from src.data_functions.data_update import Update
from src.log import logger
from src.models import User
from src.routers.auth import get_current_active_user

load_dotenv()

router = APIRouter(
    tags=["users"]
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


class UserEndpoints:
    def __init__(self, engine, model_of_user):
        self.engine = engine
        self.insert = Insert(self.engine)
        self.fetch = Fetch(self.engine)
        self.update = Update(self.engine)
        self.delete = Delete(self.engine)
        self.model_of_user = model_of_user

    @router.post('/add_user')
    async def add_user(self=None, body: dict = None):
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
            self.insert.user(self.model_of_user, username, email, first_name, last_name, hashed_password, role,
                             school_class)
        except IntegrityError:
            logger.debug("Email or username is already taken")
            raise HTTPException(
                status_code=401,
                detail="Email or username is already taken"
            )
        return Response(status_code=200, content="OK")

    @staticmethod
    @router.get("/get_user")
    async def get_user(current_user: User = Depends(get_current_active_user)):
        return current_user.username, current_user.role

    @router.get("/get_all_users")
    async def get_all_users(self=None, current_user: User = Depends(get_current_active_user)):
        if current_user.role == "admin":
            results = self.fetch.all(self.model_of_user)
        else:
            raise HTTPException(
                status_code=403,
                detail="You have no access to this endpoint"
            )
        return results

    @router.post('/update_user')
    async def update_user(self=None, body: dict = None, current_user: User = Depends(get_current_active_user)):
        updated_user = body["updated_user"]
        if updated_user["username"] == current_user.username or current_user.role == "admin":
            try:
                self.update.user(self.model_of_user, current_user.username, updated_user)
            except KeyError as er:
                logger.error(er)
                raise HTTPException(
                    status_code=400,
                    detail=f"{er}"
                )
        return Response(status_code=200, content="OK")

    @router.post("/delete_user")
    async def delete_user(self=None, body: dict = None, current_user: User = Depends(get_current_active_user)):
        username = body["username"]
        if username == current_user.username or current_user.role == "admin":
            try:
                self.delete.user(self.model_of_user, username)
            except KeyError as er:
                logger.error(er)
                raise HTTPException(
                    status_code=400,
                    detail=f"{er}"
                )
        return Response(status_code=200, content="OK")
