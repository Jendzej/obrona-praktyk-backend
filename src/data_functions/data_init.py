from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from src.log import logger
from src.models import create_models


class DataInit:
    def __init__(self, engine):
        self.engine = engine

    def create_session(self):
        session = sessionmaker(bind=self.engine)
        return session()

    def add_data(self, model):
        session = self.create_session()
        session.add(model)
        try:
            session.commit()
            session.close()
        except IntegrityError as IE:
            session.close()
            # logger.debug(IE)
            raise IE
        session.commit()
        session.close()

    def add_multiple_data(self, models: list):
        errors = []
        for model in models:
            try:
                self.add_data(model)
            except IntegrityError as ie:
                errors.append(ie)
                continue
        return errors

    def initial_insertion(self, initial_models):
        model_school_classes = initial_models[0]
        model_roles = initial_models[1]
        model_payment_status = initial_models[2]
        model_item = initial_models[3]
        data = [
            model_school_classes(school_class="1TIP"),
            model_school_classes(school_class="1TI1"),
            model_school_classes(school_class="1TI2"),
            model_school_classes(school_class="1TR"),
            model_school_classes(school_class="1TET"),
            model_school_classes(school_class="2TI1"),
            model_school_classes(school_class="2TI2"),
            model_school_classes(school_class="2TR"),
            model_school_classes(school_class="2TET"),
            model_school_classes(school_class="3TI1"),
            model_school_classes(school_class="3TI2"),
            model_school_classes(school_class="3TR"),
            model_school_classes(school_class="3TET"),
            model_school_classes(school_class="4TIP"),
            model_school_classes(school_class="4TI1"),
            model_school_classes(school_class="4TI2"),
            model_school_classes(school_class="4TR"),
            model_school_classes(school_class="4TOR"),
            model_school_classes(school_class="4TET"),
            model_school_classes(school_class="4TEP"),

            model_roles(role="admin"),
            model_roles(role="user"),

            model_payment_status(status="paid"),
            model_payment_status(status="not paid"),
            model_payment_status(status="pending"),
            model_payment_status(status="other"),

            model_item(item_name='Bulka z kurczakiem', item_price=5.5,
                       item_description='Bulka z panierowanym kurczakiem, pomidorem, salata i serem',
                       item_image_url='url'),
            model_item(item_name='Bagietka czosnkowa', item_price=2.5, item_description='Bagietka z maslem czosnkowym',
                       item_image_url='url2'),
            model_item(item_name='Drozdzowka z kruszonka', item_price=3.0,
                       item_description='Drozdzowka z kruszonka i lukrem', item_image_url='url3')
        ]
        errors = self.add_multiple_data(data)
        if len(errors) == 0:
            logger.info("Successfully added db initial data")
        else:
            logger.info("Db may contains initial data already")

    def create_tables(self, base):
        model_list = create_models(self.engine, base)
        model_school_classes = model_list[0][0]
        model_roles = model_list[0][1]
        model_payment_status = model_list[0][2]
        model_item = model_list[1][0]
        initial_models = [model_school_classes, model_roles, model_payment_status, model_item]

        try:
            self.initial_insertion(initial_models)
            logger.info("Inserted database start data")
        except IntegrityError:
            logger.info("Database start data already exists, skipping insertion")
        return model_list
