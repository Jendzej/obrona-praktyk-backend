import uvicorn
from sqlalchemy.ext.declarative import declarative_base

from src.db import db

Base = declarative_base()
db.connecting_db()
db.init.create_tables(Base)
engine = db.engine
models = db.models[1]
other_models = db.models[0]

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        reload=True,
        port=8000
    )
