from main import engine, models
from src.data_functions import session
from src.log import logger


class TransactionFunction:
    def __init__(self):
        self.session = session.create_session(engine)
        self.transaction_model = models[2]
        self.item_model = models[0]

    def get_all(self):
        """Get all transaction"""
        try:
            data = self.session.query(self.transaction_model).all()
            self.session.close()
            return data
        except:
            self.session.close()
            logger.error(er)
            return False

    def get(self, transaction_id):
        """Get transaction from database by id"""
        try:
            data = self.session.query(self.transaction_model).filter(self.transaction_model.id == transaction_id).one()
            self.session.close()
            return data
        except Exception as er:
            self.session.close()
            logger.error(er)
            return False

    def get_all_for_user(self, user_id):
        """Get all transactions from database"""
        data = self.session.query(self.transaction_model).filter(self.transaction_model.user_id == user_id).all()
        self.session.close()
        return data

    def insert(self, user_id, item_id, payment_status, transaction_time, delivery_time):
        """Add transaction to database"""
        try:
            item = self.session.query(self.item_model).filter(self.item_model.id == item_id).one()
            self.session.add(self.transaction_model(
                user_id=user_id,
                item_id=item_id,
                payment_status=payment_status,
                transaction_time=transaction_time,
                delivery_time=delivery_time,
                item_price=item.item_price
            ))
            self.session.commit()
            self.session.close()
            return True
        except Exception as er:
            self.session.close()
            logger.error(er)
            return False

    def update(self, transaction_id, new_transaction_data: dict):
        """Update transaction transaction_id with new_transaction_data"""
        try:
            part_of_transaction_to_update = self.session.query(self.transaction_model).filter(
                self.transaction_model.id == transaction_id).one()
            transaction_to_update = self.session.query(self.transaction_model).filter(
                self.transaction_model.transaction_time == part_of_transaction_to_update.transaction_time).all()

            for transaction in transaction_to_update:
                transaction.update(new_transaction_data)

            self.session.commit()
            self.session.close()
            return True
        except Exception as er:
            self.session.close()
            logger.error(er)
            return False

    def delete(self, transaction_id):
        """Delete all transactions, which have the same transaction_time as transaction with transaction_id"""
        try:
            item_of_transaction = self.session.query(self.transaction_model).filter(
                self.transaction_model.id == transaction_id).one()
            transaction = self.session.query(self.transaction_model).filter(
                self.transaction_model.transaction_time == item_of_transaction.transaction_time).all()

            for transaction_item in transaction:
                self.session.delete(transaction_item)
            self.session.commit()
            self.session.close()
            return True
        except Exception as er:
            self.session.close()
            logger.error(er)
            return False
