import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Response
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

from src.database import Database
from src.routers.auth import router as AuthRouter
from src.routers.transactions import router as TransactionsRouter

load_dotenv()
Base = declarative_base()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

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


@app.post('/users')
async def asks(body: dict):
    """Endpoint for adding users"""
    password = body['password']
    username = body['username']
    email = body['email']
    hashed_password = jwt.encode({username: password}, SECRET_KEY, ALGORITHM)
    role = 'user'
    try:
        db.insert.user(model_of_user, username, email, body['first_name'], body['last_name'], hashed_password, role,
                       body['school_class'])
    except IntegrityError:
        print("Email or username is already taken")
        raise HTTPException(
            status_code=401,
            detail="Email or username is already taken"
        )
    return Response(status_code=200, content="OK")


app.include_router(AuthRouter)
app.include_router(TransactionsRouter)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=8000
    )
