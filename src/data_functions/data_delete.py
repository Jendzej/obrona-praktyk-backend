from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker

from src.log import logger


class Delete:
    def __init__(self, engine):
        self.engine = engine

    def create_session(self):
        session = sessionmaker(bind=self.engine)
        return session()

    def item(self, item_model, item_name):
        session = self.create_session()
        try:
            session.query(item_model).filter(item_model.item_name == item_name).one()
        except NoResultFound:
            raise NoResultFound

        session.query(item_model).filter(item_model.item_name == item_name).delete()
        session.commit()
        session.close()
        logger.debug(f"Item '{item_name}' successfully deleted!")

    def user(self, user_model, username):
        session = self.create_session()
        try:
            session.query(user_model).filter(user_model.username == username).one()
        except NoResultFound:
            raise NoResultFound

        session.query(user_model).filter(user_model.username == username).delete()
        session.commit()
        session.close()
        logger.debug(f"User '{username}' successfully deleted!")

    def school_class(self, school_class_model, school_class):
        session = self.create_session()
        try:
            session.query(school_class_model).filter(school_class_model.school_class == school_class).one()
        except NoResultFound:
            raise NoResultFound

        session.query(school_class_model).filter(school_class_model.school_class == school_class).delete()
        session.commit()
        session.close()
        logger.debug(f"School class '{school_class}' successfully deleted!")

    def role(self, role_model, role):
        session = self.create_session()
        try:
            session.query(role_model).filter(role_model.role == role).one()
        except NoResultFound:
            raise NoResultFound

        session.query(role_model).filter(role_model.role == role).delete()
        session.commit()
        session.close()
        logger.debug(f"Role '{role}' successfully deleted!")

    def transaction(self, transaction_model, gr_transaction_model, transaction_time):
        session = self.create_session()

        data = session.query(transaction_model).filter(transaction_model.transaction_time == transaction_time).all()

        if len(data) != 0:
            for transaction in data:
                transaction.delete()
                self.gr_transaction(gr_transaction_model, transaction_time)
            session.commit()
            session.close()
        else:
            raise NoResultFound

    def gr_transaction(self, gr_transaction_model, transaction_time):
        session = self.create_session()
        try:
            session.query(gr_transaction_model).filter(gr_transaction_model.transaction_time == transaction_time).one()
        except NoResultFound:
            raise NoResultFound

        session.query(gr_transaction_model).filter(gr_transaction_model.transaction_time == transaction_time).delete()
        session.commit()
        session.close()
