from slacker import Slacker
import slackclient
import shelve
import time
import config
from requests.sessions import Session

# If you need to proxy the requests
bot = slackclient.SlackClient(config.token)


def main():
    if bot.rtm_connect():
        print('bot started...')
        i = 0
        while True:
            i += 1
            news = bot.rtm_read()
            for update in news:
                if 'type' in update and update['type'] == 'message' and update['text'] == '<@UBLFE0S9G> /test':
                    if i % 2 == 0:
                        bot.rtm_send_message(update['channel'], 'even')
                    else:
                        bot.rtm_send_message(update['channel'], 'odd')
            time.sleep(1)


if __name__ == '__main__':
    main()

bot. 
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
