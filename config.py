from data import db_session
from data.users import User
from data.temperature import Temperature
from data.pressure import Pressure
from data.consumption import Consumption
from data.roles import Roles


db_session.global_init("db/database.sqlite")
session = db_session.create_session()
HOST = '0.0.0.0'
PORT = 80
DEBUG = False
SECRET_KEY = 'scada_system'
REMEMBER_USER = False
COUNT_SAVED_LOGINS = 4
# TODO
TEMPLATE_REMEMBER_USERS = ['кто-то', 'кто-то', 'ещё кто-то']
# TEMPLATE_REMEMBER_USERS = []
MIN_PASSWORD_LENGTH = 6
NOTES_PAGE_SIZE = 100
NOTES_HEAD_PAGE_SIZE = 3
FLASK_ADMIN_SWATCH = 'Spacelab'


def create_root():
    root_user = session.query(User).filter(User.login == 'root').first()
    if not root_user:
        root_user = User(
            login='root',
            role_id=1
        )
        root_user.set_password('root')
        session.add(root_user)
        session.commit()


def add_default_record(table, params):
    title = params['title']
    record = session.query(table).filter(table.title == title).first()
    if record:
        return False
    new_record = table(**params)
    session.add(new_record)
    session.commit()
    return True


def create_values():
    add_default_record(Temperature, {
        'title': 'градус Цельсия',
        'desc': '°С'
    })
    add_default_record(Temperature, {
        'title': 'градус Фаренгейта',
        'desc': '°F',
        'coefficient': 9 / 5,
        'shift': 32
    })
    add_default_record(Temperature, {
        'title': 'градус Кельвина',
        'desc': 'K',
        'shift': -273.15
    })

    add_default_record(Pressure, {
        'title': 'Паскаль',
        'desc': 'Па',
    })
    add_default_record(Pressure, {
        'title': 'кгс/см²',
        'desc': 'кгс/см²',
        'coefficient': 1.01972 * 10 ** (-5)
    })
    add_default_record(Pressure, {
        'title': 'бар',
        'desc': 'бар',
        'coefficient': 1 * 10 ** (-5)
    })
    add_default_record(Pressure, {
        'title': 'атм',
        'desc': 'атм',
        'coefficient': 0.98692 * 10 ** (-5)
    })
    add_default_record(Pressure, {
        'title': 'мм рт.ст.',
        'desc': 'мм рт.ст.',
        'coefficient': 750.06 * 10 ** (-5)
    })
    add_default_record(Pressure, {
        'title': 'мм вод.ст.',
        'desc': 'мм вод.ст.',
        'coefficient': 0.101972
    })
    add_default_record(Pressure, {
        'title': 'пси',
        'desc': 'пси',
        'coefficient': 1.45 * 10 ** (-4)
    })

    add_default_record(Consumption, {
        'title': 'м³/ч',
        'desc': 'м³/ч',
        'coefficient': 1 / 3600
    })
    add_default_record(Consumption, {
        'title': 'м³/c',
        'desc': 'м³/c',
    })


def create_roles():
    add_default_record(Roles, {
        'title': 'Суперадминистратор',
        'index': 1000
    })
    add_default_record(Roles, {
        'title': 'Администратор',
        'index': 500
    })
    add_default_record(Roles, {
        'title': 'Пользователь',
        'index': 0
    })


create_roles()
create_root()
create_values()


TEMPERATURES = session.query(Temperature).all()
PRESSURES = session.query(Pressure).all()
CONSUMPTIONS = session.query(Consumption).all()
