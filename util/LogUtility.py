from datetime import datetime as dt
from traceback import print_exc

import config


class Logger:
    """Логгер, для красивого отображения всяких несчастий"""

    def __init__(self, tag):
        self.__tag = str(tag)

    def INFO(self, message, inner_tag=None):
        print("{} | INFO    | ".format(dt.now().strftime('%d, %b %Y %H:%M:%S')) + str(self.__tag), end='')

        if inner_tag is not None:
            print("." + inner_tag, end='')

        print(" : ", end='')

        print(message)

    def DEBUG(self, message, inner_tag=None):

        if not config.DEBUG_MODE:
            return

        print("{} | DEBUG   | ".format(dt.now().strftime('%d, %b %Y %H:%M:%S')) + str(self.__tag), end='')

        if inner_tag is not None:
            print("." + inner_tag, end='')

        print(" : ", end='')

        print(message)

    def ERROR(self, message, inner_tag=None):
        print("{} | ERROR   | ".format(dt.now().strftime('%d, %b %Y %H:%M:%S')) + str(self.__tag), end='')

        # Увы, такая шняга убивает поток
        # if isinstance(message, Exception):
        #     print()
        #     print_exc(message)

        if inner_tag is not None:
            print("." + inner_tag, end='')

        print(" : ", end='')

        print(message)

    def WARNING(self, message, inner_tag=None):
        print("{} | WARNING | ".format(dt.now().strftime('%d, %b %Y %H:%M:%S')) + str(self.__tag), end='')

        if inner_tag is not None:
            print("." + inner_tag, end='')

        print(" : ", end='')

        print(message)
