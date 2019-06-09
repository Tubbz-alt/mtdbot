# Slack bot for MethodPro 2018

## Installation instructions

### Slack bot registration

Press "+" button, near by "Apps"

![1](https://semior001.github.io/mtdpro_slackbot/add_app.png)

Find "Bots" application in slack apps list

![2](https://semior001.github.io/mtdpro_slackbot/find_bots_app.png)

Press "Add Configuration" button and follow instructions

![3](https://semior001.github.io/mtdpro_slackbot/new_bot.png)

### Configuration of python application

After installing Python and other required packages, you have to create a configuration
file "config.py" at the root of the project. This file should have several constants:

* BOT_TOKEN - slack bot's token, it can be shown in bot's settings page
* BOT_ID - unique identifier of the bot, it is necessary for looking on appeal to the bot
* DB_LOCATION - location of sqlite database
* DEBUG_MODE - debugging sqllite queries
* ADMIN_DATA - Dictionary object, which should have two fields, describes data for entering to the
  * login
  * password
* WEBSITE_HOST - IP address where the admin panel will be running at () 
* WEBSITE_PORT - port 

Example of this config file:
```python
# -*- coding: utf-8 -*-
import datetime

WEBSITE_HOST = "0.0.0.0"
WEBSITE_PORT = "8080"

DB_LOCATION = "db.sqlite3"

BOT_TOKEN = "xoxb-000000000000-000000000000-abc0000000000"
BOT_ID = "UK0000000"

DEBUG_MODE = True

TEACHER_AUTH_CODE = "teacher"
TA_AUTH_CODE = "ta"
SHUFFLE_SEC_CODE = "shuffle"

TEAM_SIZE = 5

ADMIN_DATA = {
    "login": "ADMIN",
    "password": "VERYPROTECTEDPASSWORD"
}

ETUDE_PERIODS = {
    "start": datetime.time(00, 00),
    "end": datetime.time(23, 00),
    "days": [True, True, True, True, True, True, True]
}
```

Then, to run a web-server, just execute the next command:

```
python3 app.py
```

## Commands
* @\<BotUsername\> /it - register user in IT group
* @\<BotUsername\> /nonit - register user in NONIT group
* @\<BotUsername\> /teacher \<TEACHER_AUTH_CODE\> - register user in TEACHER group
* @\<BotUsername\> /ta \<TA_AUTH_CODE\> - register user in TA group
* @\<BotUsername\> /coins - get user's coins
* @\<BotUsername\> /give_coins @\<recipient\> \<amount\> - transaction  
* @\<BotUsername\> /shuffle_teams \<SHUFFLE_SEC_CODE\> \<"mixed"\> - make teams, team size is defined in config.py. 
    Mixed parameter - make teams of it and nonit users. If you don't want mixed teams, just do not add this parameter

## Requirements

* Python 3.7 +
* Python packages (with versions, which are used in development):
  * flask 1.0.3
  * peewee 3.9.6
  * flask-basicauth 0.2.0
  * phial-slack 0.9.0 (it also installs slackclient package)
  * slacker 0.13.0

## Description of initial task

**Features:**

Важные:
1) Coins
2) Teams

Второстепенные:
1) Мониторинг пассивных стажеров
2) Репорты для 2го месяца

**Coins:**
1) Преподаватели могут давать coins каждому студенту во время уроков (maximum 20)
2) TA могут давать coins после проверок домашних заданий (max 15)
3) Стажеры (только во время этюдов) могут давать друг другу coins за помощь в заданиях (max 5), 
при этом у отправителя эти coins отнимаются
4) (Второстепенно) Каждая 5-ая отправка coins между стажерами не забирает coins у отправителя

**Teams:**
1) Разделение на команды стажеров равномерно не засоряя чат
2) Админка, где можно видеть список команд
3) Оценка сокомандников после работы и комментарии.
4) Report о том, чему научились

**Monitoring:**
1) Список пассивных стажеров
   * у кого мало коинов
   * у кого мало транзакций во время этюдов

**Reports:**
1) Во второй месяц капитан команды делает репорт боту о проделанной работе
2) Каждый стажер пишет, чему научились за последние два дня
3) Ставит цель на следующие два дня (стажер)  

## Authors:
* IT:
  * [Aza](https://github.com/Semior001/mtdbot/commits?author=MeBr0)
  * [Adlet](https://github.com/Semior001/mtdbot/commits?author=adiletabs)
  * [Yelshat](https://github.com/Semior001/mtdbot/commits?author=Semior001)
* Non-IT:
  * Diyara
  * Aru