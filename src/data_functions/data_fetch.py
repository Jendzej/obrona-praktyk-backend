from sqlalchemy.exc import NoResultFound
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

    def user(self, user_model, username):
        session = self.create_session()
        try:
            data = session.query(user_model).filter(user_model.username == username).one()
        except NoResultFound as er:
            raise er

        return data

    def item(self, item_model, item_name):
        session = self.create_session()
        data = session.query(item_model).filter(item_model.item_name == item_name).one()
        return data

    def users_transactions(self, transaction_model, username):
        session = self.create_session()
        data = session.query(transaction_model).filter(transaction_model.user == username).all()
        return data
