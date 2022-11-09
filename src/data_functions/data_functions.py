from sqlalchemy.orm import sessionmaker


def create_session(engine):
    sess = sessionmaker(bind=engine)
    return sess()
