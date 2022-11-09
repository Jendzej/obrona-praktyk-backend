from pydantic import BaseModel
from sqlalchemy import Sequence, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship


def create_models(engine, base):
    """Creating models in db"""
    item_id_sequence = Sequence('item_id_sequence')
    transaction_sequence = Sequence('transaction_sequence')
    user_id_sequence = Sequence('user_id_sequence')

    class Items(base):
        __tablename__ = "items"
        id = Column(Integer, item_id_sequence, primary_key=True, server_default=item_id_sequence.next_value())
        item_name = Column(String(60), unique=True)
        item_price = Column(Float)
        item_description = Column(String(300))
        item_image_url = Column(String(200))

        def __repr__(self):
            """Creating columns in table"""
            return f"<Items(id={self.id}, item_name={self.item_name}, item_price={self.item_price}, item_description={self.item_description}, item_image_url={self.item_image_url})>"

    class SchoolClasses(base):
        __tablename__ = "school_classes"
        school_class = Column(String(6), primary_key=True)

        def __repr__(self):
            """Creating column in table"""
            return f"<SchoolClasses(school_class={self.school_class})>"

    class Roles(base):
        __tablename__ = "roles"
        role = Column(String(10), primary_key=True)

        def __repr__(self):
            """Creating column in table"""
            return f"<Roles(role={self.role})>"

    class PaymentStatus(base):
        __tablename__ = "payment_status"
        status = Column(String(15), primary_key=True, unique=True)

        def __repr__(self):
            """Creating column in table"""
            return f"<PaymentStatus(status={self.status})>"

    class Users(base):
        __tablename__ = "users"
        id = Column(Integer, user_id_sequence, server_default=user_id_sequence.next_value())
        username = Column(String(20), primary_key=True)
        email = Column(String(50), unique=True)
        first_name = Column(String(30))
        last_name = Column(String(30))
        password = Column(String(150))
        role = Column(String, ForeignKey('roles.role', onupdate='CASCADE', ondelete='CASCADE'))
        school_class = Column(String, ForeignKey('school_classes.school_class', onupdate='CASCADE', ondelete='CASCADE'))
        transaction_item = relationship('Items', secondary='transactions', backref='transaction_items')

        def __repr__(self):
            return f"<Users(username={self.username}, email={self.email}, first_name={self.first_name}, last_name={self.last_name}, password={self.password}, role={self.role}, school_class={self.school_class})>"

    class Transactions(base):
        __tablename__ = "transactions"
        id = Column(Integer, transaction_sequence, primary_key=True, server_default=transaction_sequence.next_value())
        user = Column(String, ForeignKey("users.username", onupdate='CASCADE', ondelete='CASCADE'))
        item = Column(String, ForeignKey("items.item_name", onupdate='CASCADE', ondelete='CASCADE'))
        payment_status = Column(String, ForeignKey("payment_status.status"))
        transaction_time = Column(DateTime)

        def __repr__(self):
            return f"<Transactions(id={self.id}, user={self.user}, item={self.item}, payment_status={self.payment_status}, transaction_time={self.transaction_time})>"

    base.metadata.create_all(engine)
    return [[SchoolClasses, Roles, PaymentStatus], [Items, Users, Transactions]]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    mail: str
    role: str


class UserInDb(User):
    hashed_password: str
