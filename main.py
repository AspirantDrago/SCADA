from flask import Flask, redirect, request, render_template, session as flask_session
from flask_login import login_required, current_user, LoginManager, logout_user, login_user
import os
import logging

from config import *
from data.users import User
from data.temperature import Temperature
from data.pressure import Pressure
from data.consumption import Consumption
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from forms.edit_password_form import EditPasswordForm
from forms.edit_login_form import EditLoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
logging.basicConfig(level=logging.INFO)


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    print(session.query(User).all())
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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


if __name__ == '__main__':
    port_run = int(os.environ.get("PORT", PORT))
    app.run(host=HOST, port=port_run, debug=DEBAG)
