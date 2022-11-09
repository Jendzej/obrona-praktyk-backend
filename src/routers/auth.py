import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import HTTPException, Depends, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.exc import NoResultFound

from src.data_functions.data_fetch import Fetch
from src.data_functions.data_insert import Insert
from src.log import logger
from src.models import TokenData, User, UserInDb, Token

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

router = APIRouter(
    tags=['auth']
)


class Auth:
    def __init__(self, engine, model_of_user):
        self.engine = engine
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
        self.insert = Insert(self.engine)
        self.fetch = Fetch(self.engine)
        self.model_of_user = model_of_user

    def verify_password(self, username, plain_password, hashed_password):
        decoded_hashed = jwt.decode(hashed_password, self.SECRET_KEY, self.ALGORITHM)
        if decoded_hashed[username] == plain_password:
            return True
        else:
            return False

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def get_user(self, username: str):
        try:
            user = self.fetch.user(self.model_of_user, username)
        except NoResultFound:
            logger.error(f"No result found, HTTP_400_BAD_REQUEST - This username does not exist '{username}'")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This username does not exist",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return UserInDb(username=user.username, mail=user.email, role=user.role, hashed_password=user.password)

    def authenticate_user(self, username: str, password: str):
        user = self.get_user(username)
        if not user:
            return False
        if not self.verify_password(username, password, user.hashed_password):
            return False
        return user

    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                logger.error(f"{credentials_exception}")
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            logger.error(f"{credentials_exception}")
            raise credentials_exception
        user = self.get_user(username=token_data.username)
        if user is None:
            logger.error(f"{credentials_exception}")
            raise credentials_exception
        return user

    @staticmethod
    async def get_current_active_user(current_user: User = Depends(get_current_user)):
        return current_user

    @router.post("/token", response_model=Token)
    async def login_for_access_token(self, form_data: OAuth2PasswordRequestForm = Depends()):
        user = self.authenticate_user(form_data.username, form_data.password)
        if not user:
            logger.error("HTTP_401_UNAUTHORIZED - Incorrect username or password")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        access_token_expires = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}


get_current_active_user = Auth.get_current_active_user
