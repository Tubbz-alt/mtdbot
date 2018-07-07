from slacker import Slacker
import slackclient
import json
import time
import config

bot = slackclient.SlackClient(config.token)
slack = Slacker(config.token)

def get_data(type):
    data = {}
    if type == 'it':
        with open('it.json', 'r') as file:
            data = json.load(file)
    elif type == 'nonit':
        with open('nonit.json', 'r') as file:
            data = json.load(file)
    return data

def add_user(msg, user_id):
    user = slack.users.info(user_id).body['user']
    name = user['profile']['real_name']
    data_it = get_data('it')
    data_nonit = get_data('nonit')
    if (data_it.get(user_id) == None) and (data_nonit.get(user_id) == None):
        if msg == '/IT':
            data_it[user_id] = [name, 0]
            with open('it.json', 'w') as file:
                json.dump(data_it, file)
        elif msg == '/NONIT':
            data_nonit[user_id] = [name, 0]
            with open('nonit.json', 'w') as file:
                json.dump(data_nonit, file)





def main():
    if bot.rtm_connect():
        print('bot started...')
        while True:
            news = bot.rtm_read()
            for update in news:
                if 'type' in update and update['type'] == 'message':
                    message = update['text']
                    if message.split()[0] == '<@' + config.bot_id + '>':
                        if message.split()[1] == '/IT' or message.split()[1] == '/NONIT':
                            add_user(message.split(' ')[1], update['user'])
                        #update['user']
            #bot.rtm_send_message(update['channel'], update['text'])
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
