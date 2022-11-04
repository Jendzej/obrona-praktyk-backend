from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
import datetime
from src.log import logger


def create_session(engine):
    session = sessionmaker(bind=engine)
    return session()


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


def insert_user(engine, user_model, username: str, email: str, first_name: str, last_name: str, password: str, role: str, school_class: str):
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


def insert_transaction(engine, transaction_model, user: str, item: str, payment_status: str, transaction_time: datetime):
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
