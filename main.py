import slackclient
from teams import *


def get_reviews():
    with open('reviews.json', 'r') as file:
        data = json.load(file)
    return data

def get_pretty_reviews(id):
    print("trying to return reviews")
    print(id)
    data = get_reviews()
    data_it = get_data('IT')
    data_nonit = get_data('NONIT')
    text = ""

    for i in data[id]:
        text += "From: "
        try:
            text += data_it[i['from']]
        except:
            text += data_nonit[i['from']]
        text += "\n"
        text += i['body']
        text += "\n \n \n"
    with open('reviews.txt', 'w') as file:
        file.write(text)


def add_review(from_id, to_id, body):
    data = get_reviews()
    try:
        if data[to_id] is None:
            data[to_id] = []
    except:
        data[to_id] = []
    data[to_id].append({'from': from_id, 'body': body})
    with open('reviews.json', 'w') as file:
        json.dump(data, file)


bot = slackclient.SlackClient(config.token)
slack = Slacker(config.token)


def get_data(msg):
    try:
        with open(msg + '.json', 'r') as file:
            data = json.load(file)
        return data
    finally:
        pass


def get_name(user_id):
    return slack.users.info(user_id).body['user']['profile']['real_name']


def add_user(msg, user_id):
    name = get_name(user_id)

    data_it = get_data('IT')
    data_nonit = get_data('NONIT')

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
    data = get_data('admin')

    if msg == '/admin' and data.get('admin') is None:
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


def add_coins(channel, user_id, coins):
    if 15 >= int(coins) >= -5:
        user_id = user_id.replace('<', '').replace('>', '').replace('@', '')

        data = get_data(channel)
        data.get(user_id)[1] += int(coins)

        with open(channel + '.json', 'w') as file:
            json.dump(data, file)


def transfer_coins(channel, user_id1, user_id2, coins):
    data = get_data(channel)

    user_id1 = user_id1.replace('<', '').replace('>', '').replace('@', '')
    user_id2 = user_id2.replace('<', '').replace('>', '').replace('@', '')

    if (user_id1 in data) and (user_id2 in data) and 5 >= int(coins) >= 1:
        data.get(user_id2)[1] += int(coins)
        data.get(user_id1)[1] -= int(coins)

        with open(channel + '.json', 'w') as file:
            json.dump(data, file)


def my_coins(user_id, channel):
    msg = ''

    for i in slack.channels.list().body['channels']:
        if get_data(i['name']) is not None:

            if user_id in get_data('IT') and get_data(i['name']).get('type') != "NONIT":
                msg += i['name'] + ": " + str(get_data(i['name'])[user_id][1])
                msg += '\n'

            elif user_id in get_data('NONIT') and get_data(i['name']).get('type') != "IT":
                msg += i['name'] + ": " + str(get_data(i['name'])[user_id][1])
                msg += '\n'

    bot.rtm_send_message(channel, msg)

def show_lb(channel):

    data = get_data(channel)
    users = []
    # print(data)

    for i in data:
        if i != 'type':
            if type(data[i][1]) is int:
                users.append([data[i][1], data[i][0]])

    users.sort()
    users.reverse()
    print(users)

    msg = ''

    for i in users:
        msg += i[1] + " " + str(i[0]) + "\n"

    bot.rtm_send_message(channel, msg)

def main():
    if bot.rtm_connect():

        print("bot has been started")

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
                                
                        elif second == '/leaderboard':
                            for i in slack.channels.list().body['channels']:
                                if i['id'].find(update['channel']) != -1:
                                    channel = i['name']
                                    show_lb(channel)
                                    break
                                 
                        elif second == '/update':
                            data = get_data('admin')
                            third = message[2].replace('#', '')
                            third = third.split('|')[1].replace('>', '')

                            if (update['user'] in data.get('admin')) or (update['user'] in get_data(third).get(third)):
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
                                time.sleep(2)
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

                        elif second == '/my_coins':
                            my_coins(update['user'], update['channel'])

                        elif second == '/give_review':
                            print("trying to get review")
                            # if check_time(config.start_etude, config.end_etude):

                            try:
                                print("i've got it")
                                third = message[2]
                                id = third[2:-1]
                                print(id)

                                print("from: ", update['user'], " to: ", id, " body: ", update['text'])

                                teams = get_teams()

                                for i in teams:
                                    if id in teams[i]['members'] and update['user'] in teams[i]['members'] and id != update['user']:
                                        print("it works")
                                        add_review(update['user'], id, update['text'][update['text'].rindex(">") + 2:])
                            except:
                                print("oops")

                        elif second == "/get_reviews":
                            if update['user'] in get_data('admin').get('admin'):
                                try:
                                    third = message[2]
                                    get_pretty_reviews(third[2:-1])
                                    time.sleep(2)
                                    data = get_data('admin')
                                    destination = data.get('admin')
                                    slack.files.upload('reviews.txt', channels=destination)
                                except:
                                    pass




            time.sleep(1)


if __name__ == '__main__':
    main()
