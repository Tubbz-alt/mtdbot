from peewee import (
    SqliteDatabase,
    Model,
    IntegerField,
    CharField,
    TimestampField,
    ForeignKeyField,
    TextField,
    TimeField,
    SmallIntegerField,
    DoesNotExist
)
from datetime import datetime as dt

import config

db = SqliteDatabase(config.DB_LOCATION)


def init_db():
    db.connect()
    db.create_tables([
        User,
        Group,
        Transaction,
        Commentary,
        Lesson,
        Team,
        TeamHistory
    ])

    try:
        Group.get(Group.name == 'IT')
    except DoesNotExist as e:
        Group.create(
            name='IT',
            description='Группа для гикнутых'
        )

    try:
        Group.get(Group.name == 'NONIT')
    except DoesNotExist as e:
        Group.create(
            name='NONIT',
            description='Группа для сочувствующих'
        )

    try:
        Group.get(Group.name == 'TEACHER')
    except DoesNotExist as e:
        Group.create(
            name='TEACHER',
            description='Группа для мудрых'
        )

    try:
        Group.get(Group.name == 'TA')
    except DoesNotExist as e:
        Group.create(
            name='TA',
            description='Группа для заботливых'
        )


class BaseModel(Model):
    class Meta:
        database = db


class Group(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(null=False, unique=True)
    description = TextField()
    created_at = TimestampField(default=dt.now())
    updated_at = TimestampField(default=dt.now())


class Team(BaseModel):
    id = IntegerField(primary_key=True)
    created_at = TimestampField(default=dt.now())


class User(BaseModel):
    id = IntegerField(primary_key=True)
    slack_id = CharField(index=True, unique=True)
    display_name = CharField()
    real_name = CharField()
    email = CharField(unique=True, index=True)
    group = ForeignKeyField(Group, backref='users')
    coins = IntegerField(default=0)
    team = ForeignKeyField(Team, backref='members', null=True)
    created_at = TimestampField(default=dt.now())
    updated_at = TimestampField(default=dt.now())


class TeamHistory(BaseModel):
    id = IntegerField(primary_key=True)
    user = ForeignKeyField(User, backref='teams_history')
    team = ForeignKeyField(Team, backref='members_history')
    created_at = TimestampField(default=dt.now())


class Lesson(BaseModel):
    id = IntegerField(primary_key=True)
    teacher = ForeignKeyField(User, backref='lessons', null=False)
    start_time = TimeField(null=False)
    end_time = TimeField(null=False)
    weekday = SmallIntegerField(null=False)
    created_at = TimestampField(default=dt.now())
    updated_at = TimestampField(default=dt.now())


class Commentary(BaseModel):
    id = IntegerField(primary_key=True)
    type = IntegerField(null=False)  # 0 - report, 1 - what have i learned, 2 - goals
    author = ForeignKeyField(User, backref='reports_from')
    target = ForeignKeyField(User, backref='reports_about', null=True)
    text = TextField()
    created_at = TimestampField(default=dt.now())


class Transaction(BaseModel):
    id = IntegerField(primary_key=True)
    author = ForeignKeyField(User, backref='transactions_from')
    recipient = ForeignKeyField(User, backref='transactions_to')
    took = IntegerField(null=False)
    gave = IntegerField(null=False)
    created_at = TimestampField(default=dt.now())
