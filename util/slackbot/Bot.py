import threading
import time
from inspect import signature

from slackclient import SlackClient
from slacker import Slacker

from util import LogUtility
from .BotExceptions import (
    CommandNotFound,
    InvalidCommandInvocation,
    InvalidNumberOfArguments,
    BasicBotExceptionWrapper
)

logger = LogUtility.Logger("SlackBot")


class Bot(object):
    """Класс, описывающий общую концепцию взаимодействия с ботом"""

    __error_placeholders = dict()

    def __init__(self, token, bot_id):
        """Инициализация класса
        :param token: - авторизационный токен бота
        :param bot_id: - уникальный идентификатор бота в slack-workspace
        """
        self.__bot = SlackClient(token)
        self.__slack = Slacker(token)
        self.__running = True
        self.__command_handlers = dict()
        self.__bot_id = bot_id

        # Обработчики ошибок
        self.__error_placeholders[CommandNotFound.__name__] = "Команда {} не найдена!"
        self.__error_placeholders[InvalidCommandInvocation.__name__] = "Неправильный вызов команды"
        self.__error_placeholders[InvalidNumberOfArguments.__name__] = "Команда {} принимает {} аргументов"

    def set_error_placeholder(self, error_type, message):
        self.__error_placeholders[error_type] = message

    def send_message(self, channel, message):
        """
        Отправка сообщения
        :param channel: - ID канала, в который необходимо отправить сообщение
        :param message: - сообщение, собственно
        """
        self.__bot.rtm_send_message(channel, message)

    def __add_command_handler(self, command, handler):
        """Добавляет обработчик команды
        :param command: - строковое название команды
        :param handler: - функция-обработчик команды, на эту функцию будут подаваться аргументы, распарсенные из команды
        """
        if command[0] != '/':
            command = '/' + command

        self.__command_handlers[command] = handler

    def handle_update(self, bot, update):
        """Метод, реализующий обработку <b>любого</b> сообщения
        :param bot: - объект бота
        :param update: - объект события
        """
        pass

    def disconnect(self):
        """Выключает слушатель событий и завершает фоновый поток"""
        self.__running = False

    def get_user_information(self, user_id):
        """Получение информации о пользователе
        :param user_id: - уникальный идентификатор пользователя в slack-workspace
        """
        return self.__slack.users.info(user_id)

    def get_channels_list(self):
        """Получение списка каналов"""
        return self.__slack.channels.list().body['channels']

    def upload_file(self, filename, destination):
        """Загрузка файла в какой-либо канал
        :param filename: - абсолютный или относительный путь до файла, который необходимо загрузить
        :param destination: - каналы, в которые необходимо отправить файл
        """
        self.__slack.files.upload(filename, channels=destination)

    def __run_listener(self):
        """Функция-слушатель событий"""

        logger.INFO("Bot listener has been started! Bot id: " + self.__bot_id)

        while self.__running:
            news = self.__bot.rtm_read()
            for update in news:
                if ('type' in update) and (update['type'] == 'message'):
                    message = update['text'].split(' ')

                    # Проверяем, идёт ли обращение к боту
                    if message[0] == "<@" + self.__bot_id + ">":
                        if message[1][0] != '/':
                            self.__handle_error(
                                BasicBotExceptionWrapper(
                                    message[1],
                                    InvalidCommandInvocation()
                                ),
                                update['channel']
                            )
                            continue

                        # Если у нас есть обработчик на данную команду...
                        if message[1] in self.__command_handlers:
                            try:
                                # Запускаем обработчик со всеми аргументами
                                self.__command_handlers[message[1]](update, *message[2:len(message)])
                            except TypeError as e:
                                self.__handle_error(
                                    BasicBotExceptionWrapper(
                                        message[1],
                                        InvalidNumberOfArguments(
                                            len(signature(self.__command_handlers[message[1]]).parameters)
                                        )
                                    ),
                                    update['channel']
                                )
                            except Exception as e:
                                self.__handle_error(BasicBotExceptionWrapper(message[1], e), update['channel'])
                        else:
                            self.__handle_error(
                                BasicBotExceptionWrapper(
                                    message[1],
                                    CommandNotFound())
                                ,
                                update['channel']
                            )

                    self.handle_update(self, update)

            time.sleep(1)

    def command_handler(self, name):
        """Декоратор для пометки методов, как обработчиков команд"""

        def decorator(handler):
            self.__add_command_handler(name, handler)

        return decorator

    def run(self):
        """Запускает слушатель бота. Запускается в новом потоке"""
        if self.__bot.rtm_connect():
            thread = threading.Thread(target=self.__run_listener, args=(), daemon=True)
            thread.start()

    def __handle_error(self, e, channel_id):
        """Обрабатывает ошибки, происходящие во время выполнения команд"""
        if isinstance(e.exception, CommandNotFound):
            self.send_message(
                channel_id,
                self.__error_placeholders[CommandNotFound.__name__].format(e.command_name)
            )
        elif isinstance(e.exception, InvalidCommandInvocation):
            self.send_message(
                channel_id,
                self.__error_placeholders[InvalidCommandInvocation.__name__]
            )
        elif isinstance(e.exception, InvalidNumberOfArguments):
            self.send_message(
                channel_id,
                self.__error_placeholders[InvalidNumberOfArguments.__name__].format(
                    e.command_name,
                    e.exception.number_of_arguments - 1
                )
            )
