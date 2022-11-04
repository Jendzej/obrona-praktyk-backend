from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from src.log import logger


def add_data(engine, model):
    session = sessionmaker(bind=engine)
    sess = session()
    sess.add(model)
    try:
        logger.info(f"Adding data to database...")
        sess.commit()
        logger.debug(f"Successfully added data - {model}")
    except IntegrityError as IE:
        # logger.debug(IE)
        raise IE


def add_multiple_data(engine, models: list):
    for model in models:
        add_data(engine, model)


def select_user(engine, model, username):
    session = sessionmaker(bind=engine)
    sess = session()
    data = sess.query(model).filter(model.username == username).all()
    return data


def update_user(engine, user_model, username, new_user_data: dict):
    session = sessionmaker(bind=engine)
    sess = session()
    user_to_update = select_user(engine, user_model, username)
    sess.query(user_model).filter(user_model.id == user_to_update[0].id).update(new_user_data)
    sess.commit()
    return sess.query(user_model).filter(user_model.id == user_to_update[0].id).all()
