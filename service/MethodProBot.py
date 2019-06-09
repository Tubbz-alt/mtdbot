import string
from datetime import datetime as dt
from random import sample, getrandbits, choice

from peewee import IntegrityError, DoesNotExist

import config
from model import (
    UserRepository,
    TeamRepository
)
from util import Logger, Bot

logger = Logger('MethodProBot')


class MethodProBot:
    def __init__(self,
                 bot_id,  # type: str
                 bot_token  # type: str
                 ):
        self.bot = Bot(bot_id=bot_id, token=bot_token)

        # Регистрационные команды
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
                user = UserRepository.create_new_user(
                    display_name=user_info['profile']['display_name'],
                    slack_id=user_info['id'],
                    real_name=user_info['real_name'],
                    email=user_info['profile']['email'],
                    group_code='IT'
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
                user = UserRepository.create_new_user(
                    display_name=user_info['profile']['display_name'],
                    slack_id=user_info['id'],
                    real_name=user_info['real_name'],
                    email=user_info['profile']['email'],
                    group_code='NONIT'
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

        @self.bot.command_handler("teacher")
        def put_user_to_teachers_group(update, security_code):
            if security_code != config.TEACHER_AUTH_CODE:
                self.bot.send_message(
                    update['channel'],
                    "Неверный код"
                )
                return

            response = self.bot.get_user_information(update['user'])

            if not response.successful:
                self.bot.send_message(update['channel'], "Ошибка при попытке получения информации о пользователе")
                logger.ERROR("Error during  'get_user_info' procedure execution")
                return

            user_info = response.body['user']
            logger.DEBUG(user_info['profile'])

            try:
                user = UserRepository.create_new_user(
                    display_name=user_info['profile']['display_name'],
                    slack_id=user_info['id'],
                    real_name=user_info['real_name'],
                    email=user_info['profile']['email'],
                    group_code='TEACHER'
                )
                self.bot.send_message(
                    update['channel'],
                    "Пользователь <@{}> успешно добавлен в группу TEACHER"
                        .format(user.slack_id)
                )
            except IntegrityError:
                self.bot.send_message(
                    update['channel'],
                    "Пользователь <@{}> уже присутствует в базе"
                        .format(user_info['id'])
                )

        @self.bot.command_handler("test")
        def create_test_user(update):
            letters = string.ascii_lowercase
            UserRepository.create_new_user(
                display_name=''.join(choice(letters) for i in range(5)),
                slack_id=''.join(choice(letters) for i in range(5)),
                real_name=''.join(choice(letters) for i in range(5)),
                email=''.join(choice(letters) for i in range(5)),
                group_code='IT' if bool(getrandbits(1)) else 'NONIT'
            )

        @self.bot.command_handler("ta")
        def put_user_to_ta_group(update, security_code):
            if security_code != config.TA_AUTH_CODE:
                self.bot.send_message(
                    update['channel'],
                    "Неверный код"
                )
                return

            response = self.bot.get_user_information(update['user'])

            if not response.successful:
                self.bot.send_message(update['channel'], "Ошибка при попытке получения информации о пользователе")
                logger.ERROR("Error during  'get_user_info' procedure execution")
                return

            user_info = response.body['user']
            logger.DEBUG(user_info['profile'])

            try:
                user = UserRepository.create_new_user(
                    display_name=user_info['profile']['display_name'],
                    slack_id=user_info['id'],
                    real_name=user_info['real_name'],
                    email=user_info['profile']['email'],
                    group_code='TA'
                )
                self.bot.send_message(
                    update['channel'],
                    "Пользователь <@{}> успешно добавлен в группу TA"
                        .format(user.slack_id)
                )
            except IntegrityError:
                self.bot.send_message(
                    update['channel'],
                    "Пользователь <@{}> уже присутствует в базе"
                        .format(user_info['id'])
                )

        # Информационные команды
        @self.bot.command_handler("get_teams")
        def get_teams(update):
            teams = TeamRepository.get_all_teams()
            logger.DEBUG(teams)

            text = ''
            for team in teams:
                logger.DEBUG(len(list(team.members)))
                if len(list(team.members)) <= 0:
                    continue
                text += 'Team #' + str(team.id) + ':\n'
                for member in team.members:
                    text += '    ' + member.real_name + ' (' + member.display_name + ')\n'
                text += '\n'

            with open('media/teams.txt', 'w+') as file:
                file.write(text)

            self.bot.send_file(update['channel'], 'media/teams.txt')

        @self.bot.command_handler("coins")
        def show_users_coins(update):
            try:
                user = UserRepository.get_user_by_slack_id(update['user'])
            except DoesNotExist:
                self.bot.send_message(
                    update['channel'],
                    "Пользователь не найден"
                )
                return
            self.bot.send_message(
                update['channel'],
                "<@{}>, У вас {} коинов".format(update['user'], str(user.coins))
            )

        @self.bot.command_handler("give_coins")
        def give_coins_to_another_user(update, userId, amount):
            """Проведение транзакции"""
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
                author = UserRepository.get_user_by_slack_id(update['user'])
                recipient = UserRepository.get_user_by_slack_id(userId[2:-1])
            except DoesNotExist:
                self.bot.send_message(
                    update['channel'],
                    "Не найден инициатор транзакции или реципиент"
                )
                return
            except IndexError:
                self.bot.send_message(
                    update['channel'],
                    "Неправильный формат получателя. Отправляйте в виде @Username"
                )
                return

            if author == recipient:
                self.bot.send_message(
                    update['channel'],
                    "Инициатор транзакции также указан, как получатель"
                )
                return

            if author.group.name != 'IT' and author.group.name != 'NONIT' \
                    and recipient.group.name != 'IT' and recipient.group.name != 'NONIT':
                self.bot.send_message(
                    update['channel'],
                    "Оба участника транзакции не являются стажерами"
                )
                return

            now = dt.now()

            # Проверка на этюд
            if (config.ETUDE_PERIODS['days'][now.weekday()]) \
                    and (config.ETUDE_PERIODS['start'] <= now.time() <= config.ETUDE_PERIODS['end']) \
                    and (author.group.name == 'IT' or author.group.name == 'NONIT') \
                    and (recipient.group.name == 'IT' or recipient.group.name == 'NONIT') \
                    and (0 > amount or amount > 5):
                self.bot.send_message(
                    update['channel'],
                    "Сумма транзакции больше 5"
                )
                return

            # todo Проверка на текущий урок преподавателя

            count_of_transactions = UserRepository.get_count_of_user_transactions(author.id)
            took = amount

            # Если инициатор - учитель или TA или сейчас пятая транзакция то транзакция безвозмездна
            if (author.group.name == 'TEACHER' and 0 < amount <= 20) \
                    or (author.group.name == 'TA' and 0 < amount <= 15) \
                    or (count_of_transactions % 5 == 4):
                took = 0

            # Количество коинов
            if took > author.coins:
                self.bot.send_message(update['channel'],
                                      "Недостаточное количество коинов для проведения транзакции")
                return

            author.coins -= took
            author.save()

            recipient.coins += amount
            recipient.save()

            # Проводим транзакцию
            UserRepository.transfer_coins(
                author_id=author.id,
                recipient_id=recipient.id,
                take=took,
                give=amount
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

        @self.bot.command_handler("shuffle_teams")
        def shuffle_users_to_commands(update, security_code, mixed):
            """Перемешивание команд (потом будет только в админке)"""
            if security_code != config.SHUFFLE_SEC_CODE:
                self.bot.send_message(
                    update['channel'],
                    "Неверный код"
                )

            mixed = (mixed == 'mixed')

            it_users = list(UserRepository.get_it_group_users_shuffled())
            logger.DEBUG(it_users)

            nonit_users = list(UserRepository.get_nonit_group_users_shuffled())
            logger.DEBUG(nonit_users)

            current_team = []

            if not mixed:
                # Формируем IT команды
                for i, user in enumerate(it_users):
                    current_team.append(user)
                    if len(current_team) == config.TEAM_SIZE:
                        TeamRepository.register_new_team(current_team)
                        current_team = []

                if len(current_team) > 0:
                    TeamRepository.register_new_team(current_team)

                # Формируем NONIT команды
                for i, user in enumerate(nonit_users):
                    current_team.append(user)
                    if len(current_team) == config.TEAM_SIZE:
                        TeamRepository.register_new_team(current_team)
                        current_team = []

                if len(current_team) > 0:
                    TeamRepository.register_new_team(current_team)

                self.bot.send_message(update['channel'], "Команды сформированы")
                return

            while len(it_users) > int(config.TEAM_SIZE / 2) and len(nonit_users) > int(config.TEAM_SIZE / 2):
                it_part = sample(it_users, int(config.TEAM_SIZE / 2))
                nonit_part = sample(nonit_users, int(config.TEAM_SIZE / 2))

                for i in it_part:
                    it_users.remove(i)

                for i in nonit_part:
                    nonit_users.remove(i)

                current_team = it_part + nonit_part

                if config.TEAM_SIZE % 2 != 0:
                    if bool(getrandbits(1)):
                        additional_user = choice(it_users)
                        it_users.remove(additional_user)
                    else:
                        additional_user = choice(nonit_users)
                        nonit_users.remove(additional_user)
                    current_team += [additional_user]

                TeamRepository.register_new_team(current_team)

            if len(it_users) > 0 or len(nonit_users) > 0:
                TeamRepository.register_new_team(it_users + nonit_users)

            self.bot.send_message(update['channel'], "Команды сформированы")

    def run(self):
        self.bot.run()
