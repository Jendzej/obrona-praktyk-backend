from sqlalchemy.orm import sessionmaker


def create_session(engine):
    session = sessionmaker(bind=engine)
    return session()
