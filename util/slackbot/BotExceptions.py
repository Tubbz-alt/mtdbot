class BasicBotExceptionWrapper:
    """Базовый класс ошибок бота"""
    command_name = ""
    exception = None

    def __init__(self, command_name, exception):
        self.command_name = command_name
        self.exception = exception


class CommandNotFound:
    """Ошибка, сигнализирующая об отсутствии обработчика на команду"""
    pass


class InvalidCommandInvocation:
    """Неправильный вызов команды
    Вызов команды начинается с символа '/' """
    pass


class InvalidNumberOfArguments:
    """Неверное количество аргументов команды"""
    def __init__(self, number_of_arguments):
        self.number_of_arguments = number_of_arguments
