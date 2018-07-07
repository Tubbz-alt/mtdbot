from slacker import Slacker
import shelve
import config
from requests.sessions import Session

# If you need to proxy the requests
slack = Slacker(config.token)

# Send a message to #general channel
#slack.chat.post_message('#general', 'Hey there!')

response = slack.users.list()
users = response.body['members']
msg = ''
#for i in users:
#    if not i['is_bot'] and i['name'] != 'slackbot':
#        msg = msg + i['name'] + '\n'

#slack.chat.post_message('@adl.absatov', users)

# Get users list

#print(slack.auth.test()) - информация о workspace
#print(slack.channels.list()) - список всех каналов с информацией
#print(slack.channels.info('CBL8D6XGC')) - информация о канале
#print(slack.channels.history('CBL8D6XGC')) - история сообщений
#print(slack.channels.replies('CBL8D6XGC')) - информация о тредах в чате/канале
#chat.delete - удалить конкретное сообщение из чата
#chat.getPermalink - получить ссылку на канал