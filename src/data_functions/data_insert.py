import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import sessionmaker


class Insert:
    def __init__(self, engine):
        self.engine = engine

    def create_session(self):
        session = sessionmaker(bind=self.engine)
        return session()

    def data(self, model):
        session = self.create_session()
        try:
            session.commit()
            session.close()
        except IntegrityError as IE:
            raise IE

    def multiple_data(self, models: list):
        for model in models:
            self.data(model)

    def item(self, item_model, item_name: str, item_price: float, item_description: str, item_image_url: str):
        session = self.create_session()
        to_add = item_model(
            item_name=item_name,
            item_price=item_price,
            item_description=item_description,
            item_image_url=item_image_url
        )
        session.add(to_add)
        try:
            session.commit()
            session.close()
        except IntegrityError as IE:
            raise IE

    def user(self, user_model, username: str, email: str, first_name: str, last_name: str, password: str,
             role: str, school_class: str):
        session = self.create_session()
        to_add = user_model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role=role,
            school_class=school_class
        )
        session.add(to_add)
        try:
            session.commit()
            session.close()
        except IntegrityError as IE:
            raise IE

    def transaction(self, transaction_model, user: str, item: str, payment_status: str,
                    transaction_time: datetime):
        session = self.create_session()
        to_add = transaction_model(
            user=user,
            item=item,
            payment_status=payment_status,
            transaction_time=transaction_time
        )
        session.add(to_add)
        try:
            session.commit()
            session.close()
        except IntegrityError as IE:
            raise IE

    def group_transaction(self, transaction_model, item_model, gr_transaction_model, user: str,
                          status):
        session = self.create_session()
        users_transaction = session.query(transaction_model).filter(transaction_model.user == user).all()
        users_transaction.reverse()
        times = {}
        for item_in_transaction in users_transaction:
            if f"{item_in_transaction.transaction_time}" in item_in_transaction.values():
                times[f'{item_in_transaction.transaction_time}'].append(item_in_transaction.item)
            else:
                times[f'{item_in_transaction.transaction_time}'] = []
                times[f'{item_in_transaction.transaction_time}'].append(item_in_transaction.item)

        gr_transactions = session.query(gr_transaction_model).filter(gr_transaction_model.user == user).all()
        gr_times = [value.values() for value in gr_transactions]

        for key in times:
            if key not in gr_times:
                session.rollback()
                items_value: float = 0
                for data in times[key]:
                    items_value += session.query(item_model).filter(
                        item_model.item_name == data).first().item_price
                to_add = gr_transaction_model(
                    user=user,
                    items=MutableList.as_mutable(times[key]),
                    items_value=items_value,
                    payment_status=status,
                    transaction_time=key
                )
                session.add(to_add)
            try:
                session.commit()
                session.close()
            except IntegrityError as IE:
                raise IE
