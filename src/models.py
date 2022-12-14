"""Creating models for API and database"""
from fastapi import Body
from pydantic import BaseModel
from sqlalchemy import Sequence, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship


def create_models(engine, base):
    """Creating models in db"""
    item_id_sequence = Sequence('item_id_sequence')
    transaction_sequence = Sequence('transaction_sequence')
    user_id_sequence = Sequence('user_id_sequence')

    class Items(base):
        """Table to store items data"""
        __tablename__ = "items"
        id = Column(Integer, item_id_sequence,
                    primary_key=True, server_default=item_id_sequence.next_value())
        item_name = Column(String(60), unique=True)
        item_price = Column(Float)
        item_description = Column(String(300))
        item_image_url = Column(String(200))

        def __repr__(self):
            """Creating columns in table"""
            return f"<Items(id={self.id}, item_name={self.item_name}, " \
                   f"item_price={self.item_price}, item_description={self.item_description}, " \
                   f"item_image_url={self.item_image_url})>"

    class SchoolClasses(base):
        """Table to store School Classes"""
        __tablename__ = "school_classes"
        school_class = Column(String(6), primary_key=True)

        def __repr__(self):
            """Creating column in table"""
            return f"<SchoolClasses(school_class={self.school_class})>"

    class Roles(base):
        """Table to store Roles"""
        __tablename__ = "roles"
        role = Column(String(10), primary_key=True)

        def __repr__(self):
            """Creating column in table"""
            return f"<Roles(role={self.role})>"

    class PaymentStatus(base):
        """Table to store Payment Statuses"""
        __tablename__ = "payment_status"
        status = Column(String(15), primary_key=True, unique=True)

        def __repr__(self):
            """Creating column in table"""
            return f"<PaymentStatus(status={self.status})>"

    class Users(base):
        """Table to store users data"""
        __tablename__ = "users"
        id = Column(Integer, user_id_sequence, primary_key=True,
                    server_default=user_id_sequence.next_value(), unique=True)
        username = Column(String(20), primary_key=True)
        email = Column(String(50), unique=True)
        first_name = Column(String(30))
        last_name = Column(String(30))
        password = Column(String(150))
        role = Column(String,
                      ForeignKey('roles.role', onupdate='CASCADE', ondelete='CASCADE'))
        school_class = Column(String, ForeignKey('school_classes.school_class',
                                                 onupdate='CASCADE', ondelete='CASCADE'))
        transaction_item = relationship('Items', secondary='transactions',
                                        backref='transaction_items')

        def __repr__(self):
            return f"<Users(id={self.id}, username={self.username}, email={self.email}, " \
                   f"first_name={self.first_name}, last_name={self.last_name}, " \
                   f"password={self.password}, role={self.role}, school_class={self.school_class})>"

    class Transactions(base):
        """Table to store transactions data"""
        __tablename__ = "transactions"
        id = Column(Integer, transaction_sequence, primary_key=True,
                    server_default=transaction_sequence.next_value())
        user_id = Column(Integer, ForeignKey("users.id", onupdate='CASCADE', ondelete='CASCADE'))
        item_id = Column(Integer, ForeignKey("items.id", onupdate='CASCADE', ondelete='CASCADE'))
        payment_status = Column(String, ForeignKey("payment_status.status"))
        transaction_time = Column(DateTime)
        delivery_time = Column(DateTime)
        item_price = Column(Float)

        def __repr__(self):
            return f"<Transactions(id={self.id}, user_id={self.user_id}, item_id={self.item_id}, " \
                   f"payment_status={self.payment_status}, transaction_time={self.transaction_time}, " \
                   f"delivery_time={self.delivery_time}, item_price={self.item_price})>"

    base.metadata.create_all(engine)
    return [[SchoolClasses, Roles, PaymentStatus], [Items, Users, Transactions]]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    id: int
    username: str
    mail: str
    role: str


example_User = Body(example={
    "username": "user",
    "email": "email",
    "first_name": "First",
    "last_name": "Last",
    "password": "password",
    "school_class": "4TIP"
})

example_Item = Body(example={
    "item_name": "item1",
    "item_price": 4.5,
    "item_description": "Description of item 1",
    "item_image_url": "url1"
})

example_Transaction = Body(example={
    "items": [1, 2, 3],
    "payment_status": "paid",
    "del_time": "2022-11-18 10:30"
})
