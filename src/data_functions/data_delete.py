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
            logger.error(f"Cannot find item '{item_name}'")
            return

        session.query(item_model).filter(item_model.item_name == item_name).delete()
        session.commit()
        logger.debug(f"Item '{item_name}' successfully deleted!")

    def user(self, user_model, username):
        session = self.create_session()
        try:
            session.query(user_model).filter(user_model.username == username).one()
        except NoResultFound:
            logger.error(f"Cannot find user '{username}'")
            return

        session.query(user_model).filter(user_model.username == username).delete()
        session.commit()
        logger.debug(f"User '{username}' successfully deleted!")

    def school_class(self, school_class_model, school_class):
        session = self.create_session()
        try:
            session.query(school_class_model).filter(school_class_model.school_class == school_class).one()
        except NoResultFound:
            logger.error(f"Cannot find school class '{school_class}'")
            return

        session.query(school_class_model).filter(school_class_model.school_class == school_class).delete()
        session.commit()
        logger.debug(f"School class '{school_class}' successfully deleted!")

    def role(self, role_model, role):
        session = self.create_session()
        try:
            session.query(role_model).filter(role_model.role == role).one()
        except NoResultFound:
            logger.error(f"Cannot find role '{role}'")
            return

        session.query(role_model).filter(role_model.role == role).delete()
        session.commit()
        logger.debug(f"Role '{role}' successfully deleted!")

    def transaction(self, transaction_model, transaction_time):
        session = self.create_session()
        try:
            session.query(transaction_model).filter(transaction_model.transaction_time == transaction_time).one()
        except NoResultFound:
            logger.error(f"Cannot find transaction at '{transaction_time}'")
            return

        session.query(transaction_model).filter(transaction_model.transaction_time == transaction_time).delete()
        session.commit()
        logger.debug(f"Transaction at '{transaction_time}' successfully deleted!")

    def gr_transaction(self, gr_transaction_model, transaction_time):
        session = self.create_session()
        try:
            session.query(gr_transaction_model).filter(gr_transaction_model.transaction_time == transaction_time).one()
        except NoResultFound:
            logger.error(f"Cannot find gr_transaction at '{transaction_time}'")
            return

        session.query(gr_transaction_model).filter(gr_transaction_model.transaction_time == transaction_time).delete()
        session.commit()
        logger.debug(f"Grouped transaction at '{transaction_time}' successfully deleted!")
