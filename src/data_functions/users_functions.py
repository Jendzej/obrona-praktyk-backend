from main import engine, models
from src.data_functions import session
from src.log import logger
from src.routers.auth import create_access_token, decode_password


class UserFunction:
    def __init__(self):
        self.session = session.create_session(engine)
        self.user_model = models[1]

    def get(self, user_id):
        """Get user from database by id"""
        try:
            data = self.session.query(self.user_model).filter(self.user_model.id == user_id).one()
            self.session.close()
            return data
        except Exception as er:
            self.session.close()
            logger.error(er)
            return False

    def get_all(self):
        """Get all users from database"""
        data = self.session.query(self.user_model).all()
        self.session.close()
        return data

    def insert(self, username, email, first_name, last_name, password, role, school_class, raise_err=False):
        """Add user to database"""
        try:
            self.session.add(self.user_model(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                role=role,
                school_class=school_class
            ))
            self.session.commit()
            self.session.close()
            return True
        except Exception as er:
            self.session.close()
            if raise_err:
                raise er
            else:
                logger.error(er)
                return False

    def update(self, user_id, new_user_data: dict):
        """Update user with new_user_data. If new_user_data (dict) contains username - password
        is updated too (because of JWT token, which is generating from dict {username: password}). Returns boolean"""
        try:
            user_to_update = self.session.query(self.user_model).filter(self.user_model.id == user_id).one()
            if 'username' in new_user_data.keys():
                if 'password' in new_user_data.keys():
                    new_user_data['password'] = create_access_token(
                        {new_user_data['username']: new_user_data['password']})
                else:
                    old_password = decode_password(user_to_update.password)
                    new_user_data['password'] = create_access_token(
                        {new_user_data['username']: old_password[user_to_update.username]})
            else:
                if 'password' in new_user_data.keys():
                    new_user_data['password'] = create_access_token(
                        {user_to_update.username: new_user_data['password']})
            self.session.query(self.user_model).filter(self.user_model.id == user_id).update(new_user_data)
            self.session.commit()
            self.session.close()
            return True
        except Exception as er:
            self.session.close()
            logger.error(er)
            return False

    def delete(self, user_id):
        try:
            user_to_del = self.session.query(self.user_model).filter(self.user_model.id == user_id)
            user_to_del.delete()
            self.session.commit()
            self.session.close()
            return True
        except Exception as er:
            self.session.close()
            logger.error(er)
            return False
