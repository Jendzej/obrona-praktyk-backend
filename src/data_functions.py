from sqlalchemy.orm import sessionmaker

from src.log import logger


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
