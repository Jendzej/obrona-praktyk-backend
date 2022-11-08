import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.declarative import declarative_base

from src.database import Database
from src.routers.auth import router as authentication_router
from src.routers.transactions import router as transaction_router
from src.routers.users import router as user_router

load_dotenv()
Base = declarative_base()

# CONNECTING TO DB
db = Database(os.getenv("POSTGRES_USER"), os.getenv("POSTGRES_PASSWORD"), os.getenv("POSTGRES_HOST"),
              os.getenv("POSTGRES_PORT"), os.getenv("POSTGRES_DB"))
db.connecting_db()

# MODELS
db.init.create_tables(Base)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv('FRONTEND_ORIGIN'),
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"]
)

app.include_router(authentication_router)
app.include_router(transaction_router)
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=8000
    )

"""
SAMPLE USER BODY (DICT)
{
"username":"user",
"email":"email",
"first_name":"First",
"last_name":"Last",
"password":"password",
"school_class":"4TIP"
}
"""
