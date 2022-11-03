from sqlalchemy.orm import sessionmaker


def add_data(engine, model):
    session = sessionmaker(bind=engine)
    sess = session()
    sess.add(model)
    sess.commit()


def add_multiple_data(engine, models: list):
    session = sessionmaker(bind=engine)
    sess = session()

    for model in models:
        sess.add(model)

    sess.commit()
