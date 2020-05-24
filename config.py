from data import db_session
from data.users import User


db_session.global_init("db/database.sqlite")
session = db_session.create_session()
HOST = '0.0.0.0'
PORT = 80
DEBAG = True
SECRET_KEY = 'scada_system'
REMEMBER_USER = False
COUNT_SAVED_LOGINS = 4
# TODO
TEMPLATE_REMEMBER_USERS = ['кто-то', 'кто-то', 'ещё кто-то']
# TEMPLATE_REMEMBER_USERS = []


def create_root():
    root_user = session.query(User).filter(User.login == 'root').first()
    if not root_user:
        root_user = User(
            login='root'
        )
        root_user.set_password('root')
        session.add(root_user)
        session.commit()


create_root()
