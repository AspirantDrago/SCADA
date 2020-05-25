from flask import Flask, redirect, request, render_template, session as flask_session
from flask_login import login_required, current_user, LoginManager, logout_user, login_user
import os
import logging

from config import *
from data.users import User
from forms.login_form import LoginForm
from forms.register_form import RegisterForm


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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


if __name__ == '__main__':
    port_run = int(os.environ.get("PORT", PORT))
    app.run(host=HOST, port=port_run, debug=DEBAG)
