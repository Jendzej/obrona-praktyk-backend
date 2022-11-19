import os

from dotenv import load_dotenv
from jose import jwt
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def create_session(engine):
    session = sessionmaker(bind=engine)
    return session()


def update_item(engine, item_model, item_id, new_item_data: dict):
    session = create_session(engine)
    try:
        item_to_update = session.query(item_model).filter(item_model.id == item_id).one()
    except NoResultFound as er:
        raise er
    session.query(item_model).filter(item_model.id == item_to_update.id).update(new_item_data)
    session.commit()
    session.close()


def update_user(engine, user_model, user_id, new_user_data: dict, password=None):
    session = create_session(engine)
    try:
        user_to_update = session.query(user_model).filter(user_model.id == user_id).one()
    except NoResultFound as er:
        raise er
    if user_to_update.username != new_user_data["username"] and 'username' in new_user_data.keys():
        if 'password' in new_user_data.keys():
            new_user_data["password"] = jwt.encode({new_user_data["username"]: new_user_data["password"]}, SECRET_KEY,
                                                   ALGORITHM)
        else:
            new_user_data["password"] = jwt.encode({new_user_data["username"]: password}, SECRET_KEY, ALGORITHM)

    session.query(user_model).filter(user_model.id == user_id).update(new_user_data)
    session.commit()
    session.close()
