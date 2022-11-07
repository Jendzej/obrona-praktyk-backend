import os
from datetime import timedelta, datetime

from fastapi import HTTPException, status
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound

from src.data_functions.data_fetch import Fetch


class Authorization:
    def __init__(self, engine, user_model):
        self.secret_key = os.getenv("SECRET_KEY")
        self.algorithm = os.getenv("ALGORITHM")
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.engine = engine
        self.fetch = Fetch(self.engine)
        self.user_model = user_model

    class Token(BaseModel):
        access_token: str
        token_type: str

    class TokenData(BaseModel):
        username: str | None = None

    class User(BaseModel):
        username: str
        mail: str

    class UserInDb(User):
        hashed_password: str

    def verify_password(self, username, plain_password, hashed_password):
        decoded_hashed = jwt.decode(hashed_password, self.secret_key, self.algorithm)
        if decoded_hashed[username] == plain_password:
            return True
        else:
            return False

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def get_user(self, username: str):
        try:
            user = self.fetch.user(self.user_model, username)
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='This username does not exist',
                headers={'WWW-Authenticate': "Bearer"}
            )
        return self.UserInDb(username=user.username, mail=user.mail, hashed_password=user.password)

    def authenticate_user(self, username: str, password: str):
        user = self.get_user(username)
        if not user:
            return False
        if not self.verify_password(username, password, user.hashed_password):
            return False
        return user

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
