from flask import Flask
# Инициализация Flask
from flask_basicauth import BasicAuth

import config
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
basic_auth = BasicAuth(app)

# Инициализация БД
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_LOCATION
if config.DEBUG_MODE:
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

bot = MethodProBot(bot_id=config.BOT_ID, bot_token=config.BOT_TOKEN)

init_db()


def run():
    bot.run()
    app.run(host=config.WEBSITE_HOST, port=config.WEBSITE_PORT, debug=False, use_reloader=False)


if __name__ == '__main__':
    run()
