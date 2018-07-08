from slacker import Slacker
import slackclient
import json
import time
import config
from teams import *

bot = slackclient.SlackClient(config.token)
slack = Slacker(config.token)

def get_data(msg):
    try:
        with open(msg + '.json', 'r') as file:
            data = json.load(file)
        return data
    except:
        pass

def get_name(id):
    user = slack.users.info(id).body['user']
    return user['profile']['real_name']

def add_user(msg, user_id):
    name = get_name(user_id)
    try:
        data_it = get_data('IT')
        data_nonit = get_data('NONIT')
    except:
        pass

    if data_it.get(user_id) is None and data_nonit.get(user_id) is None:
        if msg == '/IT':
            data_it[user_id] = name
            with open('IT.json', 'w+') as file:
                json.dump(data_it, file)
        elif msg == '/NONIT':
            data_nonit[user_id] = name
            with open('NONIT.json', 'w+') as file:
                json.dump(data_nonit, file)

def add_admin(msg, user_id):
    print('function started')
    data = get_data('admin')
    if msg == '/admin':
        if data.get('admin') is None:
            data['admin'] = user_id
    with open('admin.json', 'w+') as file:
        json.dump(data, file)

def create_channel(channel, teacher_id, ta_id, type):
    teacher_id = teacher_id.replace('<', '').replace('>', '').replace('@', '')
    ta_id = ta_id.replace('<', '').replace('>', '').replace('@', '')
    channel = channel.replace('#', '')
    teacher_name = get_name(teacher_id)
    ta_name = get_name(ta_id)
    data = {teacher_id: [teacher_name, 't'], ta_id: [ta_name, 'ta'], 'type': type}
    channel = channel.split('|')[1].replace('>', '')
    with open(channel + '.json', 'w+') as file:
        json.dump(data, file)

def update_channel(subject):
    data = get_data(subject)
    type = data.get('type')
    if type == 'IT' or type == 'NONIT':
        db = get_data(type)
        for i in db:
            if i not in data:
                name = get_name(i)
                data[i] = [name, 0]
        with open(subject + '.json', 'w') as file:
            json.dump(data, file)
    elif type == 'BOTH':
        db = get_data("IT")
        for i in db:
            if i not in data:
                name = get_name(i)
                data[i] = [name, 0]
        db2 = get_data("IT")
        for i in db2:
            if i not in data:
                name = get_name(i)
                data[i] = [name, 0]
        with open(subject + '.json', 'w') as file:
            json.dump(data, file)

def add_coins(channel, id, coins):
    if int(coins) <= 15 and int(coins) >= -5:
        id = id.replace('<', '').replace('>', '').replace('@', '')
        data = get_data(channel)
        data.get(id)[1] += int(coins)

        with open(channel + '.json', 'w') as file:
            json.dump(data, file)

def transfer_coins(channel, id1, id2, coins):
    data = get_data(channel)
    id1 = id1.replace('<', '').replace('>', '').replace('@', '')
    id2 = id2.replace('<', '').replace('>', '').replace('@', '')
    if (id1 in data) and (id2 in data) and int(coins) <= 5 and int(coins) >= 1:
        data.get(id2)[1] += int(coins)
        data.get(id1)[1] -= int(coins)
        with open(channel + '.json', 'w') as file:
            json.dump(data, file)

def my_coins(id):
    msg = ''

    for i in slack.channels.list().body['channels']:
        if get_data(i['name']) != None:
            if id in get_data('IT') and get_data(i['name']) != None and get_data(i['name']).get('type') != "NONIT":
                msg += i['name'] + ": " + str(get_data(i['name'])[id][1])
                msg += '\n'
            elif id in get_data('NONIT') and get_data(i['name']).get('type') != "IT":
                msg += i['name'] + ": " + str(get_data(i['name'])[id][1])
                msg += '\n'

    bot.rtm_send_message(id, msg)


def main():
    if bot.rtm_connect():
        print('bot started...')
        while True:
            news = bot.rtm_read()
            for update in news:
                if 'type' in update and update['type'] == 'message':
                    message = update['text'].split(' ')
                    if message[0] == '<@' + config.bot_id + '>':
                        second = message[1]
                        if second == '/IT' or second == '/NONIT':
                            add_user(second, update['user'])
                        elif second == '/admin':
                            add_admin(second, update['user'])
                        elif second == '/set_channel':
                            data = get_data('admin')
                            if update['user'] in data.get('admin'):
                                third = message[2]
                                fourth = message[3]
                                fifth = message[4]
                                sixth = message[5]
                                create_channel(third, fourth, fifth, sixth)
                        elif second == '/update':
                            data = get_data('admin')
                            third = message[2].replace('#', '')
                            third = third.split('|')[1].replace('>', '')
                            if (update['user'] in data.get('admin')) or update['user'] in get_data(third).get(third):
                                update_channel(third)
                        elif second == '/create_teams':
                            if update['user'] in get_data('admin').get('admin'):
                                try:
                                    third = message[2]
                                    if third == 'mixed':
                                        split_teams()
                                    else:
                                        split_teams(False)
                                except:
                                    split_teams(False)
                        elif second == '/get_teams':
                            if update['user'] in get_data('admin').get('admin'):
                                get_teams_with_names()
                                data = get_data('admin')
                                destination = data.get('admin')
                                slack.files.upload('teams.txt', channels=destination)
                        elif second == '/add_coins':
                            for i in slack.channels.list().body['channels']:
                                if i['id'].find(update['channel']) != -1:
                                    third = message[2]
                                    fourth = message[3]
                                    channel = i['name']
                                    if get_data(channel)[update['user']][1] == 'ta':
                                        add_coins(channel, third, fourth)
                                        break
                                    elif get_data(channel)[update['user']][1] == 't':
                                        add_coins(channel, third, fourth)
                                        break
                        elif second == '/give_coins':
                            for i in slack.channels.list().body['channels']:
                                if i['id'].find(update['channel']) != -1:
                                    third = message[2]
                                    fourth = message[3]
                                    channel = i['name']
                                    transfer_coins(channel, update['user'], third, fourth)
                                    break
                        elif second == '/my_team':
                            data = get_data('teams')
                            text = 'Hey! This is your team for the current week: \n'
                            team = ''
                            for i in data:
                                if update['user'] in data[i]['members']:
                                    team = data[i]['members']
                                    break
                            print(team)
                            for i in team:
                                text += get_name(i) + '\n'
                            slack.chat.post_message(channel=update['user'], text = text)
                            print('done')
                        elif second == '/my_coins':
                            my_coins(update['user'])
            time.sleep(1)

if __name__ == '__main__':
    main()

# Send a message to #general channel
# slack.chat.post_message('#general', 'Hey there!')

# response = slack.users.list()
# users = response.body['members']
# msg = ''
# for i in users:
#    if not i['is_bot'] and i['name'] != 'slackbot':
#        msg = msg + i['name'] + '\n'

# slack.chat.post_message('@adl.absatov', users)

# Get users list

# print(slack.auth.test()) - информация о workspace
# print(slack.channels.list()) - список всех каналов с информацией
# print(slack.channels.info('CBL8D6XGC')) - информация о канале
# print(slack.channels.history('CBL8D6XGC')) - история сообщений
# print(slack.channels.replies('CBL8D6XGC')) - информация о тредах в чате/канале
# chat.delete - удалить конкретное сообщение из чата
# chat.getPermalink - получить ссылку на канал
# slack.chat.me_message(config.general_id, 'Yelshat')
# slack.chat.post_message('#general', 'Aza')
