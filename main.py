import os

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy.ext.declarative import declarative_base

from src.database import Database

load_dotenv()
Base = declarative_base()

app = FastAPI()

db = Database(os.getenv("POSTGRES_USER"), os.getenv("POSTGRES_PASSWORD"), os.getenv("POSTGRES_HOST"),
              os.getenv("POSTGRES_PORT"), os.getenv("POSTGRES_DB"))
db.connecting_db()

model_list = db.create_tables(Base)
model_of_item = model_list[0]
model_of_user = model_list[1]
model_of_transaction = model_list[2]
