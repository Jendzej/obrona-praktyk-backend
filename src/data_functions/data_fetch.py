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


def fetch_user_by_username(engine, user_model, username):
    session = create_session(engine)
    try:
        data = session.query(user_model).filter(user_model.username == username).one()
    except NoResultFound as er:
        raise er

    return data


def fetch_user_by_id(engine, user_model, user_id):
    session = create_session(engine)
    try:
        data = session.query(user_model).filter(user_model.id == user_id).one()
    except NoResultFound as er:
        raise er
    return data


def fetch_item(engine, item_model, item_id):
    session = create_session(engine)
    try:
        data = session.query(item_model).filter(item_model.id == item_id).one()
    except NoResultFound as er:
        raise er
    return data


def fetch_users_transactions(engine, transaction_model, user_id):
    session = create_session(engine)
    try:
        data = session.query(transaction_model).filter(transaction_model.user_id == user_id).all()
    except NoResultFound as er:
        raise er
    return data
