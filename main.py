from flask import Flask, redirect, request, render_template, session as flask_session, jsonify
from flask_login import login_required, current_user, LoginManager, logout_user, login_user
import os
import logging
from flask_admin import Admin
from flask_babelex import Babel

from config import *
from data.users import User
from data.notes import Note
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from forms.edit_password_form import EditPasswordForm
from forms.edit_login_form import EditLoginForm
from functions import *
from admin_view import *


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
logging.basicConfig(level=logging.INFO)
# set optional bootswatch theme
# app.config['FLASK_ADMIN_SWATCH'] = FLASK_ADMIN_SWATCH
admin = Admin(app, template_mode='bootstrap3', name='Административная панель')
admin.add_view(UserAdminModelView(User, session, name='Пользователи'))
admin.add_view(RoleAdminModelView(Roles, session, name='Роли'))
admin.add_view(ValuesAdminModelView(Consumption, session, name='расход',
                                    category='Единицы измерения'))
admin.add_view(ValuesAdminModelView(Temperature, session, name='температура',
                                    category='Единицы измерения'))
admin.add_view(ValuesAdminModelView(Pressure, session, name='давление',
                                    category='Единицы измерения'))
admin.add_view(NotesAdminModelView(Note, session, name='Заметки'))
babel = Babel(app)


@babel.localeselector
def get_locale():
        return 'ru'


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(request.args.get('next', '/'))
    form = LoginForm()
    if 'last_logins' not in flask_session:
        flask_session['last_logins'] = TEMPLATE_REMEMBER_USERS
    if form.validate_on_submit():
        login = form.login.data.strip()
        password = form.password.data.strip()
        user = session.query(User).filter(User.login == login).first()
        if user and user.check_password(password):
            if login in flask_session['last_logins']:
                flask_session['last_logins'].remove(login)
            flask_session['last_logins'].append(login)
            flask_session['last_logins'] = flask_session['last_logins'][-COUNT_SAVED_LOGINS:]
            flask_session.modified = True
            login_user(user, remember=REMEMBER_USER)
            return redirect(request.args.get('next', '/'))
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    login = request.args.get('login', '')
    form.login.data = login
    last_logins = flask_session['last_logins'][::-1]
    return render_template('login.html', form=form, login=login, last_logins=last_logins)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect("/")
    form = RegisterForm()
    if form.validate_on_submit():
        login = form.login.data.strip()
        password = form.password.data.strip()
        user = session.query(User).filter(User.login == login).first()
        if user:
            return render_template('register.html',
                                   message="Пользователь с таким логином уже зарегистрирован",
                                   form=form)
        new_user = User(login=login)
        new_user.set_password(password)
        session.add(new_user)
        session.commit()
        login_user(new_user, remember=REMEMBER_USER)
        return redirect('/')
    return render_template('register.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        try:
            temperature_id = int(request.form.get('temperature', '1'))
            current_user.temperature_id = temperature_id
            session.commit()
        except BaseException as e:
            pass
        try:
            pressure_id = int(request.form.get('pressure', '1'))
            current_user.pressure_id = pressure_id
            session.commit()
        except BaseException as e:
            pass
        try:
            consumption_id = int(request.form.get('consumption', '1'))
            current_user.consumption_id = consumption_id
            session.commit()
        except BaseException as e:
            pass
        try:
            consumption_type = request.form.get('consumptionType', 'reduced')
            current_user.reduced_consumption = consumption_type == 'reduced'
            session.commit()
        except BaseException as e:
            pass
    ip_address = request.remote_addr
    return render_template('profile.html',
                           ip_address=ip_address,
                           TEMPERATURES=TEMPERATURES,
                           PRESSURES=PRESSURES,
                           CONSUMPTIONS=CONSUMPTIONS
                           )


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('settings.html',
                           password_alert=request.args.get('password_alert'),
                           password_success=request.args.get('password_success'),
                           login_alert=request.args.get('login_alert'),
                           login_success=request.args.get('login_success'),
                           )


@app.route('/edit_password', methods=['GET', 'POST'])
@login_required
def edit_password():
    form = EditPasswordForm()
    if form.validate_on_submit():
        user = session.query(User).get(current_user.id)
        last_password = form.last_password.data.strip()
        if not user.check_password(last_password):
            return render_template('edit_password.html', form=form,
                                   message='Введён неправильный старый пароль')
        password = form.password.data.strip()
        if last_password == password:
            return render_template('edit_password.html', form=form,
                                   message='Старый и новый пароли совпадают')
        user.set_password(password)
        session.commit()
        return redirect('/settings?password_success=Пароль успешно изменён')
    return render_template('edit_password.html', form=form)


@app.route('/edit_login', methods=['GET', 'POST'])
@login_required
def edit_login():
    form = EditLoginForm()
    if form.validate_on_submit():
        user = session.query(User).get(current_user.id)
        login = form.new_login.data.strip()
        other_user = session.query(User).filter(User.login == login).first()
        if user == other_user:
            return render_template('edit_login.html', form=form,
                                   message='Старый и новый логины совпадают')
        if other_user:
            return render_template('edit_login.html', form=form,
                                   message='Этот логин уже занят')
        user.login = login
        session.commit()
        return redirect('/settings?login_success=Логин успешно изменён')
    return render_template('edit_login.html', form=form)


@app.route('/stand', methods=['GET'])
@login_required
def stand():
    return render_template('stand.html',
                           stand_url=get_stand_url())


@app.route('/notes', methods=['GET'])
@login_required
def notes():
    page = 1
    records = session.query(Note)\
        .filter(Note.user == current_user)\
        .order_by(Note.created_date.desc())\
        .offset(NOTES_PAGE_SIZE * (page - 1))\
        .limit(NOTES_PAGE_SIZE)\
        .all()
    return render_template('notes.html', records=records)


@app.route('/notes/<int:id>', methods=['GET', 'POST'])
@login_required
def get_note(id):
    record = session.query(Note).get(id)
    if not record:
        redirect('/')
    if record.user != current_user:
        redirect('/')
    if request.method == 'POST':
        record.data = request.form.get('text', '')
        session.commit()
        return redirect('/notes')
    return render_template('note.html',
                       text=record.data,
                       date=record.created_date_format,
                       current_record=True
                       )


@app.route('/notes/new', methods=['GET', 'POST'])
@login_required
def create_note():
    if request.method == 'POST':
        text = request.form.get('text', '')
        if text:
            record = Note(
                user=current_user,
                data=text
            )
            session.add(record)
            session.commit()
        return redirect('/notes')
    return render_template('note.html',
                       current_record=False
                       )


@app.route('/notes/remove/<int:id>', methods=['GET'])
@login_required
def notes_remove(id):
    record = session.query(Note).get(id)
    if not record:
        return jsonify({'error': 'Note not found'})
    if record.user != current_user:
        return jsonify({'error': 'No access'})
    session.delete(record)
    session.commit()
    return jsonify({'success': 'ok'})


@app.route('/headquarters', methods=['GET'])
@login_required
def headquarters():
    page = 1
    records = session.query(Note) \
        .filter(Note.user == current_user) \
        .order_by(Note.created_date.desc()) \
        .offset(NOTES_HEAD_PAGE_SIZE * (page - 1)) \
        .limit(NOTES_HEAD_PAGE_SIZE) \
        .all()
    return render_template('headquarters.html',
                           records=records
    )


@app.route('/graphs', methods=['GET'])
@app.route('/graphs/<mode>', methods=['GET'])
@login_required
def graphs(mode='temperature'):
    time_interval = chart_time_interval()
    vals = {
        'temperature': {
            'color': 'red',
            'item': 't',
            'title': 'Температура',
            'desc': current_user.temperature.desc,
        },
        'pressure': {
            'color': 'blue',
            'item': 'p',
            'title': 'Давление',
            'desc': current_user.pressure.desc,
        },
        'consumption_fact': {
            'color': 'green',
            'item': 'F',
            'title': 'Расход фактический',
            'desc': current_user.consumption.desc,
        },
        'temperature_reduce': {
            'color': 'green',
            'item': 'F',
            'title': 'Расход приведённый',
            'desc': current_user.consumption.desc,
        },
    }


    return render_template('graphs.html',
                           time_interval=time_interval,
                           mode=mode,
                           val=vals[mode]
    )


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


def get_stand_url():
    return '/static/svg/stand.svg'


if __name__ == '__main__':
    port_run = int(os.environ.get("PORT", PORT))
    app.run(host=HOST, port=port_run, debug=DEBUG)
