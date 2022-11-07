from sqlalchemy.orm import sessionmaker


class Fetch:
    def __init__(self, engine):
        self.engine = engine

    def create_session(self):
        session = sessionmaker(bind=self.engine)
        return session()

    def last(self, model):
        session = self.create_session()
        data = session.query(model).first()
        return data

    def all(self, model):
        session = self.create_session()

        data = session.query(model).all()
        return data
