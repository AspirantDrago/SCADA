from flask import Flask, redirect, request, render_template
from flask_login import login_required, current_user, LoginManager
import os
import logging

from config import *
from data.users import User


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
    if current_user.is_authenticated:
        return redirect(request.args.get('next', '/'))
    return render_template('login.html')


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')


if __name__ == '__main__':
    port_run = int(os.environ.get("PORT", PORT))
    app.run(host=HOST, port=port_run, debug=DEBAG)
