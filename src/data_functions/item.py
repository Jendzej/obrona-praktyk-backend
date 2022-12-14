"""Functions to add/delete/edit/fetch users from database"""
from main import engine, models
from src.data_functions import session
from src.log import logger


class ItemFunction:
    def __init__(self):
        self.session = session.create_session(engine)
        self.item_model = models[0]

    def get(self, item_id):
        """Get item from database by id"""
        try:
            data = self.session.query(self.item_model).filter(self.item_model.id == item_id).one()
            self.session.close()
            return data
        except Exception as er:
            self.session.close()
            logger.error(er)
            return False

    def get_all(self):
        """Get all items from database"""
        data = self.session.query(self.item_model).all()
        self.session.close()
        return data

    def insert(self, item_name, item_price, item_description, item_image_url, skip_err=False):
        """Add item to database"""
        try:
            self.session.add(self.item_model(
                item_name=item_name,
                item_price=item_price,
                item_description=item_description,
                item_image_url=item_image_url
            ))
            self.session.commit()
            self.session.close()
            return True
        except Exception as er:
            self.session.close()
            if not skip_err:
                logger.error(er)
            return False

    def update(self, item_id, new_item_data: dict):
        """Update item with new_item_data. Returns bool -
         False when error, True when successfully updated"""
        try:
            self.session.query(self.item_model).filter(
                self.item_model.id == item_id).update(new_item_data)
            self.session.commit()
            self.session.close()
            return True
        except Exception as er:
            self.session.close()
            logger.error(er)
            return False

    def delete(self, item_id):
        try:
            item_to_del = self.session.query(self.item_model).filter(self.item_model.id == item_id)
            item_to_del.delete()
            self.session.commit()
            self.session.close()
            return True
        except Exception as er:
            self.session.close()
            logger.error(er)
            return False
