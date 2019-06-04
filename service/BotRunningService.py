import config
from util.Bot import Bot


def handle_update(update):
    pass


def build_bot():
    bot = Bot(bot_id=config.BOT_ID, token=config.BOT_TOKEN)
    bot.handle_update = handle_update
    bot.run()
