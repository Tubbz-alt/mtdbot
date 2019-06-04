import threading
import time

from slackclient import SlackClient
from slacker import Slacker


class Bot:
    """Класс, описывающий общую концепцию взаимодействия с ботом"""
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

    def add_command_handler(self, command, handler):
        """Добавляет обработчик команды
        :param command: - строковое название команды
        :param handler: - функция-обработчик команды, на эту функцию будут подаваться аргументы, распарсенные из команды
        """
        if command[0] != '/':
            command = '/' + command

        self.__command_handlers[command] = handler

    def handle_update(self, update):
        """Метод, реализующий обработку <b>любого</b> сообщения
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
        while self.__running:
            news = self.__bot.rtm_read()
            for update in news:
                message = update["text"].split(' ')

                # Проверяем, идёт ли обращение к боту
                if message[0] == "<@" + self.__bot_id + ">":
                    # Если у нас есть обработчик на данную команду...
                    if message[1] in self.__command_handlers:
                        try:
                            self.__command_handlers[message[1]](*message[2:len(message)])
                        except TypeError:
                            # На случай, если пользователь дал больше аргументов, чем обработчик переваривает
                            pass

                self.handle_update(update)

            time.sleep(1)

    def run(self):
        """Запускает слушатель бота. Запускается в новом потоке"""
        if self.__bot.rtm_connect():
            thread = threading.Thread(self.__run_listener(), args=())
            thread.start()
