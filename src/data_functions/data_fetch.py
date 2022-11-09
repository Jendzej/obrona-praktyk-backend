from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker


def create_session(engine):
    session = sessionmaker(bind=engine)
    return session()


def fetch_last(engine, model):
    session = create_session(engine)
    try:
        data = session.query(model).first()
    except NoResultFound as er:
        raise er
    return data


def fetch_all(engine, model):
    session = create_session(engine)
    try:
        data = session.query(model).all()
    except NoResultFound as er:
        raise er
    return data


def fetch_user(engine, user_model, username):
    session = create_session(engine)
    try:
        data = session.query(user_model).filter(user_model.username == username).one()
    except NoResultFound as er:
        raise er

    return data


def fetch_item(engine, item_model, item_name):
    session = create_session(engine)
    try:
        data = session.query(item_model).filter(item_model.item_name == item_name).one()
    except NoResultFound as er:
        raise er
    return data


def fetch_users_transactions(engine, transaction_model, username):
    session = create_session(engine)
    try:
        data = session.query(transaction_model).filter(transaction_model.user == username).all()
    except NoResultFound as er:
        raise er
    return data
