import config
from util import LogUtility
from util.slackbot import Bot

"""Модуль сборки бота
Вешает обработчики сообщений и базовую информацию

<b>Важно!</b>
При создании обработчиков команд, необходимо указать аргументы *args и **kwargs
для избежания TypeError
"""

logger = LogUtility.Logger("BotRunningService")


def build_bot():
    """Сборка бота"""
    bot = Bot(bot_id=config.BOT_ID, token=config.BOT_TOKEN)

    print(bot.get_channels_list())

    @bot.command_handler("test")
    def handle_test(update, group):
        bot.send_message(update['channel'], 'echo ' + group)
        logger.DEBUG(bot.get_user_information(update['user']))

    @bot.command_handler("main_channel")
    def handle_main_channel(update):
        pass

    @bot.command_handler("bla")
    def handle_bla(update):
        bot.send_message(update['channel'], "wtf")

    bot.run()
