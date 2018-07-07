from slacker import Slacker
import shelve
import config
from requests.sessions import Session

# If you need to proxy the requests
slack = Slacker(config.token)

# Send a message to #general channel
slack.chat.post_message('#general', 'Hello fellow slackers!')

# Get users list
response = slack.users.list()
users = response.body['members']
print(users)
