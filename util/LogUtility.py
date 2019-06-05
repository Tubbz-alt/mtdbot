class Logger:
    """Логгер, для красивого отображения всяких несчастий"""
    def __init__(self, tag):
        self.__tag = str(tag)

    def INFO(self, message, inner_tag=None):
        print("INFO    | " + str(self.__tag), end='')

        if inner_tag is not None:
            print("." + inner_tag, end='')

        print(" : ", end='')

        print(message)

    def DEBUG(self, message, inner_tag=None):
        print("DEBUG   | " + str(self.__tag), end='')

        if inner_tag is not None:
            print("." + inner_tag, end='')

        print(" : ", end='')

        print(message)

    def ERROR(self, message, inner_tag=None):
        print("ERROR   | " + str(self.__tag), end='')

        if inner_tag is not None:
            print("." + inner_tag, end='')

        print(" : ", end='')

        print(message)

    def WARNING(self, message, inner_tag=None):
        print("WARNING | " + str(self.__tag), end='')

        if inner_tag is not None:
            print("." + inner_tag, end='')

        print(" : ", end='')

        print(message)
