import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker


def create_session(engine):
    session = sessionmaker(bind=engine)
    return session()


def insert_data(engine, model):
    session = create_session(engine)
    session.add(model)
    try:
        session.commit()
        session.close()
    except IntegrityError as IE:
        raise IE


def insert_multiple_data(engine, models: list):
    for model in models:
        insert_data(engine, model)


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
        session.commit()
        session.close()
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
        session.commit()
        session.close()
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
        session.commit()
        session.close()
    except IntegrityError as IE:
        raise IE
