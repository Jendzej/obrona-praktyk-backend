from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from src.log import logger


def add_data(engine, model):
    session = sessionmaker(bind=engine)
    sess = session()
    sess.add(model)
    try:
        logger.info(f"Adding data to database...")
        sess.commit()
        logger.debug(f"Successfully added data - {model}")
    except IntegrityError as IE:
        logger.debug(IE)
        raise IE


def add_multiple_data(engine, models: list):
    for model in models:
        add_data(engine, model)
