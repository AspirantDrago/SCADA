from flask import Flask
from flask_login import login_required
import os

from config import *


app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])


if __name__ == '__main__':
    port_run = int(os.environ.get("PORT", PORT))
    app.run(host=HOST, port=port_run, debug=DEBAG)
