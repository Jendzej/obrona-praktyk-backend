from sqlalchemy.orm import sessionmaker


def fetch_last(engine, model):
    session = sessionmaker(bind=engine)
    sess = session()

    data = sess.query(model).first()
    return data
