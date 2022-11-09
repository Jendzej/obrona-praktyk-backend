from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker


def create_session(engine):
    session = sessionmaker(bind=engine)
    return session()


def update_item(engine, item_model, item_name, new_item_data: dict):
    session = create_session(engine)
    try:
        item_to_update = session.query(item_model).filter(item_model.item_name == item_name).one()
    except NoResultFound as er:
        raise er
    session.query(item_model).filter(item_model.id == item_to_update.id).update(new_item_data)
    session.commit()
    session.close()


def update_user(engine, user_model, username, new_user_data: dict):
    session = create_session(engine)
    try:
        user_to_update = session.query(user_model).filter(user_model.username == username).one()
    except NoResultFound as er:
        raise er
    session.query(user_model).filter(user_model.id == user_to_update.id).update(new_user_data)
    session.commit()
    session.close()
