from flask import Flask
# Инициализация Flask
from flask_basicauth import BasicAuth

import config
from blueprints import main
from model.models import (init_db)
from service import MethodProBot

app = Flask(
    __name__,
    static_folder='static',
    static_url_path='',
    template_folder='templates'
)

# Инициализация basic-auth для admin-панели
app.config['BASIC_AUTH_USERNAME'] = config.ADMIN_DATA['login']
app.config['BASIC_AUTH_PASSWORD'] = config.ADMIN_DATA['password']
app.config['BASIC_AUTH_FORCE'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = config.DEBUG_MODE
basic_auth = BasicAuth(app)

# Инициализация БД
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_LOCATION
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.DEBUG_MODE

bot = MethodProBot(bot_id=config.BOT_ID, bot_token=config.BOT_TOKEN)

init_db()

# Регистрируем View'шки
app.register_blueprint(main)


def run():
    bot.run()
    app.run(host=config.WEBSITE_HOST, port=config.WEBSITE_PORT, debug=False, use_reloader=False)


if __name__ == '__main__':
    run()
