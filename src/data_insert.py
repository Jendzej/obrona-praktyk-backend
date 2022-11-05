import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import sessionmaker

from src.log import logger


def create_session(engine):
    session = sessionmaker(bind=engine)
    return session()


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


def insert_item(engine, item_model, item_name: str, item_price: float, item_description: str, item_image_url: str):
    session = create_session(engine)
    to_add = item_model(
        item_name=item_name,
        item_price=item_price,
        item_description=item_description,
        item_image_url=item_image_url
    )
    session.add(to_add)
    try:
        logger.info(f"Adding data to database...")
        session.commit()
        logger.debug(f"Successfully added data - {to_add}")
    except IntegrityError as IE:
        raise IE


def insert_user(engine, user_model, username: str, email: str, first_name: str, last_name: str, password: str,
                role: str, school_class: str):
    session = create_session(engine)
    to_add = user_model(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=password,
        role=role,
        school_class=school_class
    )
    session.add(to_add)
    try:
        logger.info(f"Adding data to database...")
        session.commit()
        logger.debug(f"Successfully added data - {to_add}")
    except IntegrityError as IE:
        raise IE


def insert_transaction(engine, transaction_model, user: str, item: str, payment_status: str,
                       transaction_time: datetime):
    session = create_session(engine)
    to_add = transaction_model(
        user=user,
        item=item,
        payment_status=payment_status,
        transaction_time=transaction_time
    )
    session.add(to_add)
    try:
        logger.info(f"Adding data to database...")
        session.commit()
        logger.debug(f"Successfully added data - {to_add}")
    except IntegrityError as IE:
        raise IE


def group_transaction(engine, transaction_model, gr_transaction_model, item_model, user: str,
                      transaction_time: datetime):
    session = create_session(engine)
    users_transaction = session.query(transaction_model).filter(transaction_model.user == user).all()
    items_value: float = 0
    items = []
    times = {}
    for item_in_transaction in users_transaction:
        data = session.query(item_model).filter(
            item_model.item_name == item_in_transaction.item).first().item_price
        items_value += data
        items.append(item_in_transaction.item)
        if item_in_transaction.transaction_time not in times:
            times[f'{item_in_transaction.transaction_time}'] = []
            times[f'{item_in_transaction.transaction_time}'].append(item_in_transaction.item)

    print(f"Items: {items}")
    print(f"Type: {type(items)}")
    to_add = gr_transaction_model(
        user=user,
        items=MutableList.as_mutable(items),
        items_value=items_value,
        transaction_time=transaction_time
    )
    session.add(to_add)
    try:
        logger.info(f"Adding data to database...")
        session.commit()
        logger.debug(f"Successfully added data - {to_add}")
    except IntegrityError as IE:
        raise IE
