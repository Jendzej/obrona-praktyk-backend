import datetime
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

from src.database import Database

load_dotenv()
Base = declarative_base()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv('FRONTEND_ORIGIN'),
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"]
)

# CONNECTING TO DB
db = Database(os.getenv("POSTGRES_USER"), os.getenv("POSTGRES_PASSWORD"), os.getenv("POSTGRES_HOST"),
              os.getenv("POSTGRES_PORT"), os.getenv("POSTGRES_DB"))
db.connecting_db()

# MODELS
model_list = db.init.create_tables(Base)

model_of_item = model_list[0]
model_of_user = model_list[1]
model_of_transaction = model_list[2]
model_of_gr_transaction = model_list[3]

db.delete.item(model_of_item, 'item1')
db.delete.user(model_of_user, 'user1')


@app.post('/user')
async def user(body: dict):
    """Endpoint for adding user"""
    hashed_password = jwt.encode({body['username']: body['password']}, os.getenv('SECRET_KEY'), os.getenv('ALGORITHM'))
    role = 'user'
    try:
        db.insert.user(model_of_user, body['username'], body['email'], body['first_name'], body['last_name'],
                       hashed_password, role, body['school_class'])
    except IntegrityError:
        raise HTTPException(
            status_code=401,
            detail="Email or username are already taken"
        )
    return Response(status_code=200, content='OK')


@app.post('/add_transaction')
async def add_item_to_transaction(body: dict):
    # user, items: list, payment_status
    user: str = body['user']
    items: list = body['items']
    payment_status: str = body['payment_status']
    transaction_time: datetime = datetime.datetime.today()
    for item in items:
        db.insert.transaction(model_of_transaction(user=user, item=item, payment_status=payment_status,
                                                   transaction_time=transaction_time))
    db.insert.group_transaction(model_of_transaction, model_of_gr_transaction, model_of_item, user, transaction_time)


@app.post('/users')
async def asks(body: dict):
    """Endpoint for adding users"""
    password = body['password']
    username = body['username']
    mail = body['mail']
    hashed_password = jwt.encode({username: password}, SECRET_KEY, ALGORITHM)
    try:
        create_session_user(engine, UserModel, mail, hashed_password, username)
    except IntegrityError:
        print("Email or username is already taken")
        raise HTTPException(
            status_code=401,
            detail="Email or username is already taken"
        )
    return Response(status_code=200, content="OK")


""" Authorization part of backend """

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(username, plain_password, hashed_password):
    decoded_hashed = jwt.decode(hashed_password, SECRET_KEY, ALGORITHM)
    if decoded_hashed[username] == plain_password:
        return True
    else:
        return False


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    users = engine.execute(f"SELECT username, mail, hashed_password FROM users WHERE username = '{username}'")
    results = users.fetchall()
    try:
        user = results[0]
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username does not exist",
            headers={"WWW-Authenticate": "Bearer"}
        )
    # user_model = User(username=user[0], mail=user[1])
    return UserInDb(username=user[0], mail=user[1], hashed_password=user[2])


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(username, password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends()):  # form_data:OAuth2PasswordRequestForm = Depends()
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=TOKEN_EXPIRE)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=8000
    )
