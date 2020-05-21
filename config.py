from data import db_session


db_session.global_init("db/database.sqlite")
session = db_session.create_session()
HOST = '0.0.0.0'
PORT = 80
DEBAG = True
SECRET_KEY = 'scada_system'



