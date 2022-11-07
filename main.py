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
from src.routers import auth

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


app.include_router(auth.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=8000
    )
