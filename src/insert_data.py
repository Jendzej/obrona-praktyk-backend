from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError


def add_data(engine, model):
    session = sessionmaker(bind=engine)
    sess = session()
    sess.add(model)
    try:
        sess.commit()
    except IntegrityError:
        print(IntegrityError)
        pass


def add_multiple_data(engine, models: list):
    for model in models:
        add_data(engine, model)
