from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker

from src.log import logger


def create_session(engine):
    session = sessionmaker(bind=engine)
    return session()


def delete_item(engine, item_model, item_name):
    session = create_session(engine)
    try:
        session.query(item_model).filter(item_model.item_name == item_name).one()
    except NoResultFound:
        raise NoResultFound

    session.query(item_model).filter(item_model.item_name == item_name).delete()
    session.commit()
    session.close()
    logger.debug(f"Item '{item_name}' successfully deleted!")


def delete_user(engine, user_model, username):
    session = create_session(engine)
    try:
        session.query(user_model).filter(user_model.username == username).one()
    except NoResultFound:
        raise NoResultFound

    session.query(user_model).filter(user_model.username == username).delete()
    session.commit()
    session.close()
    logger.debug(f"User '{username}' successfully deleted!")


def delete_school_class(engine, school_class_model, school_class):
    session = create_session(engine)
    try:
        session.query(school_class_model).filter(school_class_model.school_class == school_class).one()
    except NoResultFound:
        raise NoResultFound

    session.query(school_class_model).filter(school_class_model.school_class == school_class).delete()
    session.commit()
    session.close()
    logger.debug(f"School class '{school_class}' successfully deleted!")


def delete_role(engine, role_model, role):
    session = create_session(engine)
    try:
        session.query(role_model).filter(role_model.role == role).one()
    except NoResultFound:
        raise NoResultFound

    session.query(role_model).filter(role_model.role == role).delete()
    session.commit()
    session.close()
    logger.debug(f"Role '{role}' successfully deleted!")


def delete_transaction(engine, transaction_model, transaction_time):
    session = create_session(engine)

    data = session.query(transaction_model).filter(transaction_model.transaction_time == transaction_time).all()

    for transaction in data:
        transaction.delete()
