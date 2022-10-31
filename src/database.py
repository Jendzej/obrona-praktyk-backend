import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import time


class Database:
    def __init__(self, db_user, db_password, db_host, db_port, db_name):
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name

    def connecting_db(self):
        engine = create_engine(f"postgresql://{self.db_user}:{self.db_password}\
        @{self.db_host}:{self.db_port}/{self.db_name}")
        counter = 0
        while True:
            try:
                engine.connect()
                print(counter)
                return engine
            except:
                counter += 1
                print("Trying again ...")
                time.sleep(2)
                continue


load_dotenv()
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
name = os.getenv("POSTGRES_DB")
db = Database(user, password, host, port, name)
print(db.connecting_db())
