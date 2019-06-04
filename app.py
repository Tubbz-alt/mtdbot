from flask import Flask, render_template
from flask_basicauth import BasicAuth
from flask_sqlalchemy import SQLAlchemy

import config

app = Flask(
    __name__,
    static_folder='static',
    static_url_path='',
    template_folder='templates'
)
db = SQLAlchemy()

app.config['BASIC_AUTH_USERNAME'] = config.ADMIN_DATA['login']
app.config['BASIC_AUTH_PASSWORD'] = config.ADMIN_DATA['password']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

basic_auth = BasicAuth(app)
db.init_app(app)


@basic_auth.required
def catch_all(path):
    return render_template('index.html')
    # return 'You want path: %s' % path


if __name__ == '__main__':
    app.run(host=config.WEBSITE_HOST, port=config.WEBSITE_PORT, debug=True) # todo в продакшне убрать на false
