from main import engine, other_models
from src.data_functions import session


class StatusRoleFunctions:
    def __init__(self):
        self.session = session.create_session(engine)
        self.payment_status_model = other_models[2]
        self.role_model = other_models[1]

    def insert_role(self, role):
        try:
            self.session.add(self.role_model(
                role=role
            ))
            self.session.commit()
            self.session.close()
            return True
        except Exception as er:
            self.session.close()
            return False

    def insert_status(self, status):
        try:
            self.session.add(self.payment_status_model(
                status=status
            ))
            self.session.commit()
            self.session.close()
            return True
        except Exception as er:
            self.session.close()
            return False
