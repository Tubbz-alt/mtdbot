from peewee import IntegrityError, DoesNotExist, fn

from datetime import datetime as dt

import config
from model import User, Group, Transaction
from model.models import Lesson
from util import Logger, Bot

logger = Logger('MethodProBot')


class MethodProBot:
    def __init__(self,
                 bot_id,  # type: str
                 bot_token  # type: str
                 ):
        self.bot = Bot(bot_id=bot_id, token=bot_token)

        @self.bot.command_handler("give_coins")
        def give_coins_to_another_user(update, userId, amount):
            # Разбираемся с форматом суммы транзакции
            try:
                amount = int(amount)
                if amount <= 0 or amount > 5:
                    self.bot.send_message(
                        update['channel'],
                        "Неправильный формат суммы перечисления"
                    )
                    return
            except TypeError:
                self.bot.send_message(
                    update['channel'],
                    "Неправильный формат суммы перечисления"
                )
                return

            # Проверяем, есть ли оба в базе
            try:
                author = User.join(Lesson).join(Group).get(User.slack_id == update['user'])
                recipient = User.join(Group).get(User.slack_id == userId[2:-1])
            except DoesNotExist:
                self.bot.send_message(
                    update['channel'],
                    "Не найден инициатор транзакции или реципиент"
                )
                return
            except IndexError:
                self.bot.send_message(
                    update['channel'],
                    "Неправильный формат получателя. Отправляйте в виде @<Username>"
                )
                return

            now = dt.now()

            # Проверка на текущий урок преподавателя
            is_authors_lesson = Lesson.select(fn.EXISTS(
                (Lesson.teacher == author) &
                (Lesson.start_time <= now.time()) &
                (Lesson.end_time >= now.time()) &
                (Lesson.weekday == now.weekday())
            ))

            # todo проверка на TA

            # Проверка на этюды
            if (config.ETUDE_PERIODS['days'][now.weekday()]) \
                    and (config.ETUDE_PERIODS['start'] <= now.time() <= config.ETUDE_PERIODS['end']) \
                    and (author.group.name == 'IT' or author.group.name == 'NONIT') \
                    and (recipient.group.name == 'IT' or recipient.group.name == 'NONIT') \
                    and (author != recipient) \
                    and (0 < amount <= 5):

                # Проверяем, какая по счёту транзакция у отправителя
                count_of_transactions = Transaction.select(fn.COUNT(Transaction.author == author)).scalar()

                if count_of_transactions % 4 == 0:
                    took = 0
                else:
                    took = amount

                if took > author.coins:
                    self.bot.send_message(update['channel'],
                                          "Недостаточное количество коинов для проведения транзакции")
                    return

                author.coins -= took
                author.save()

                recipient.coins += amount
                recipient.save()

                # Проводим транзакцию
                Transaction.create(
                    author=author,
                    recipient=recipient,
                    took=took,
                    gave=amount
                )

                self.bot.send_message(
                    update['channel'],
                    "Транзакция от пользователя <@{}> пользователю <@{}> в размере {} - {} успешно завершена"
                        .format(
                        author.slack_id,
                        recipient.slack_id,
                        took,
                        amount
                    )
                )
                return
            else:
                self.bot.send_message(
                    update['channel'],
                    "Одна из следующих ошибок:\n" +
                    "• Сейчас не время этюда\n" +
                    "• Не время занятия\n" +
                    "• Участники транзакции не являются стажерами\n" +
                    "• Автор является реципиентом\n" +
                    "• Размер транзакции (во время этюда) составляет больше 5 коинов\n"
                )
                return

        @self.bot.command_handler("it")
        def put_user_to_it_group(update):
            response = self.bot.get_user_information(update['user'])

            if not response.successful:
                self.bot.send_message(update['channel'], "Ошибка при попытке получения информации о пользователе")
                logger.ERROR("Error during  'get_user_info' procedure execution")
                return

            user_info = response.body['user']
            logger.DEBUG(user_info['profile'])

            try:
                user = User.create(
                    display_name=user_info['profile']['display_name'],
                    slack_id=user_info['id'],
                    real_name=user_info['real_name'],
                    email=user_info['profile']['email'],
                    group=Group.get(Group.name == 'IT')
                )
                self.bot.send_message(
                    update['channel'],
                    "Пользователь <@{}> успешно добавлен в группу IT"
                        .format(user.slack_id)
                )
            except IntegrityError:
                self.bot.send_message(
                    update['channel'],
                    "Пользователь <@{}> уже присутствует в базе"
                        .format(user_info['id'])
                )

        @self.bot.command_handler("nonit")
        def put_user_to_nonit_group(update):
            response = self.bot.get_user_information(update['user'])

            if not response.successful:
                self.bot.send_message(update['channel'], "Ошибка при попытке получения информации о пользователе")
                logger.ERROR("Error during  'get_user_info' procedure execution")
                return

            user_info = response.body['user']
            logger.DEBUG(user_info['profile'])

            try:
                user = User.create(
                    display_name=user_info['profile']['display_name'],
                    slack_id=user_info['id'],
                    real_name=user_info['real_name'],
                    email=user_info['profile']['email'],
                    group=Group.get(Group.name == 'NONIT')
                )
                self.bot.send_message(
                    update['channel'],
                    "Пользователь <@{}> успешно добавлен в группу NONIT"
                        .format(user.slack_id)
                )
            except IntegrityError:
                self.bot.send_message(
                    update['channel'],
                    "Пользователь <@{}> уже присутствует в базе"
                        .format(user_info['id'])
                )

    def run(self):
        self.bot.run()
