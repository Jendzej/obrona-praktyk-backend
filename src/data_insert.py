from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
import datetime
from src.log import logger


def create_session(engine):
    session = sessionmaker(bind=engine)
    return session()


def insert_transation(engine, transaction_model, user: str, items: list, payment_status: str, transaction_time: datetime):
    session = create_session(engine)

    to_add = transaction_model(
        user=user,
        item=items,
        payment_status=payment_status,
        transaction_time=transaction_time
    )
    session.add(to_add)

    try:
        logger.info(f"Adding data to database...")
        session.commit()
        logger.debug(f"Successfully added data - {to_add}")
    except IntegrityError as IE:
        # logger.debug(IE)
        raise IE
