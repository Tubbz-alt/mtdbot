from peewee import fn

from model import (
    User,
    Group,
    Transaction
)
from datetime import datetime as dt


def get_all():
    return User.select(
        User.activated
    )


def unregister(user_id):
    user = User.get(User.id == user_id)
    user.activated = False
    return update_user(user)


def create_new_user(
        display_name,  # type: str
        slack_id,  # type: str
        real_name,  # type: str
        email,  # type: str
        group_code  # type: str
):
    return User.create(
        display_name=display_name,
        slack_id=slack_id,
        real_name=real_name,
        email=email,
        group=Group.get(Group.name == group_code.upper())
    )


def get_user_by_slack_id(
        slack_id  # type: str
):
    return User.get(
        (User.slack_id == slack_id) &
        User.activated
    )


def get_count_of_user_transactions(
        user_id  # type: int
):
    return Transaction.select(fn.COUNT(Transaction.author_id == user_id)).scalar()


def get_it_group_users_shuffled():
    it_group = Group.get(Group.name == "IT")
    return User.select().where(
        (User.group_id == it_group.id) &
        User.activated
    ).order_by('RAND()')


def get_nonit_group_users_shuffled():
    nonit_group = Group.get(Group.name == "NONIT")
    return User.select().where(
        (User.group_id == nonit_group.id) &
        User.activated
    ).order_by('RAND()')


def update_user(
        user  # type: User
):
    user.updated_at = dt.now()
    user.save()


def transfer_coins(
        author_id,  # type: int
        recipient_id,  # type: int
        take,  # type: int
        give  # type: int
):
    return Transaction.create(
        author_id=author_id,
        recipient_id=recipient_id,
        took=take,
        gave=give
    )
