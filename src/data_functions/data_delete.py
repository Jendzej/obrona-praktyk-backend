from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker


def create_session(engine):
    session = sessionmaker(bind=engine)
    return session()


def delete_item(engine, item_model, item_id):
    session = create_session(engine)
    try:
        item_to_del = session.query(item_model).filter(item_model.id == item_id)
    except NoResultFound:
        raise NoResultFound

    item_to_del.delete()
    session.commit()
    session.close()


def delete_user(engine, user_model, user_id):
    session = create_session(engine)
    try:
        user_to_del = session.query(user_model).filter(user_model.id == user_id)
    except NoResultFound:
        raise NoResultFound

    user_to_del.delete()
    session.commit()
    session.close()


def delete_school_class(engine, school_class_model, school_class):
    session = create_session(engine)
    try:
        session.query(school_class_model).filter(school_class_model.school_class == school_class).one()
    except NoResultFound:
        raise NoResultFound

    session.query(school_class_model).filter(school_class_model.school_class == school_class).delete()
    session.commit()
    session.close()


def delete_role(engine, role_model, role):
    session = create_session(engine)
    try:
        session.query(role_model).filter(role_model.role == role).one()
    except NoResultFound:
        raise NoResultFound

    session.query(role_model).filter(role_model.role == role).delete()
    session.commit()
    session.close()


def delete_transaction(engine, transaction_model, transaction_id):
    session = create_session(engine)

    one_transaction = session.query(transaction_model).filter(transaction_model.id == transaction_id).one()

    data = session.query(transaction_model).filter(
        transaction_model.transaction_time == one_transaction.transaction_time).all()

    for transaction in data:
        session.query(transaction_model).filter(transaction_model.id == transaction.id).delete()

    session.commit()
    session.close()
