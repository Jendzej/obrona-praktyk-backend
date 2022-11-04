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


def select_all_data(engine, model):
    session = sessionmaker(bind=engine)
    sess = session()
    data = sess.query(model).all()
    return data


def select_user(engine, model, username):
    session = sessionmaker(bind=engine)
    sess = session()
    data = sess.query(model).filter(model.username == username).all()
    if len(data) == 0:
        logger.info("Wrong parameters, can't find item")
        return False
    return data[0]


def select_item(engine, model, item_name):
    session = sessionmaker(bind=engine)
    sess = session()
    data = sess.query(model).filter(model.item_name == item_name).all()
    if len(data) == 0:
        logger.info("Wrong parameters, can't find item")
        raise
    return data[0]


def select_transaction_items(engine, transaction_model, username):
    session = sessionmaker(bind=engine)
    sess = session()
    transactions = sess.query(transaction_model).filter(transaction_model.user == username).all()
    return transactions


def update_user(engine, user_model, username, new_user_data: dict):
    session = sessionmaker(bind=engine)
    sess = session()
    user_to_update = select_user(engine, user_model, username)
    sess.query(user_model).filter(user_model.id == user_to_update.id).update(new_user_data)
    sess.commit()
    return sess.query(user_model).filter(user_model.id == user_to_update.id).all()


def update_item(engine, item_model, item_name, new_item_data: dict):
    session = sessionmaker()
    sess = session()
    item_to_update = select_item(engine, item_model, item_name)
    sess.query(item_model).filter(item_model.id == item_to_update.id).update(new_item_data)
    sess.commit()
    return sess.query(item_model).filter(item_model.id == item_to_update.id).all()
