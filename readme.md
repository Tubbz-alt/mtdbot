# Slack bot for MethodPro 2018

## Installation instructions

After installing Python and other required packages, you have to create a configuration
file "config.py" at the root of the project. This file should have several constants:

* BOT_TOKEN - slack bot's token, it can be shown in bot's settings page
* BOT_ID - unique identifier of the bot, it is necessary for looking on appeal to the bot  
* ADMIN_DATA - Dictionary object, which should have two fields, describes data for entering to the
admin panel:
  * login
  * password

Example of this config file:
```python
BOT_TOKEN = "xoxb-000000000000-000000000000-A1A1A1A1A1A1A1A1A1A1A1A1"
BOT_ID = "AA00AAA0A"

ADMIN_DATA = {
    "login": "ADMIN",
    "password": "VERYPROTECTEDPASSWORD"
}
```

Then, to run a web-server, just run the next command:

```
python3 app.py
```

## Requirements

* Python 3.7 +
* Python packages (with versions, which are used in development):
  * flask 1.0.3
  * flask-basicauth 0.2.0
  * flask-sqlalchemy 0.8.0
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