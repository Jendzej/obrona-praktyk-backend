"""Database initiation, models (tables) creation, run fastapi server on `python run`"""
import json

import uvicorn
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base

from src.db import db

load_dotenv()

Base = declarative_base()
db.connecting_db()
engine = db.engine
models = db.models[1]
other_models = db.models[0]

with open('startup_data.json', 'r', encoding='UTF-8') as startup_data_file:
    startup_data = json.load(startup_data_file)
    startup_class, startup_roles, startup_status, startup_items = startup_data.values()

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        reload=True,
        port=8000
    )
