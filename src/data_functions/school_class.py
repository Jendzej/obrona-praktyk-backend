from main import engine, other_models
from src.data_functions import session
from src.log import logger


class SchoolClassFunction:
    def __init__(self):
        self.session = session.create_session(engine)
        self.school_class_model = other_models[0]

    def get_all(self):
        data = self.session.query(self.school_class_model).all()
        self.session.close()
        return data

    def insert(self, school_class, skip_err=False):
        try:
            self.session.add(self.school_class_model(
                school_class=school_class
            ))
            self.session.commit()
            self.session.close()
            return True
        except Exception as er:
            self.session.close()
            if not skip_err:
                logger.error(er)
            return False
