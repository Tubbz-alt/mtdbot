import json
from slacker import Slacker
import random
import time
import config
from teams import *

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


def get_teams():
    with open('teams.json', 'r') as file:
        data = json.load(file)
    return data


def get_teams_with_names():
    data = get_teams()
    data_it = get_data('it')
    data_nonit = get_data('nonit')

    for i in data:
        members_names = []
        print("data_information", i)
        for j in data[i]['members']:

            try:
                members_names.append(data_it[j][0])
            except:
                members_names.append(data_nonit[j][0])

        data[i]['members'] = members_names

    with open('teams.txt', 'w') as file:
        file.write(json.dumps(data, indent=4, sort_keys=True))


def add_team(team):
    # to add to teams file
    data = get_teams()
    print("trying to add team to database: ", team)
    try:
        data[team['id']] = {'type': team['type'], 'members': team['members']}
    except:
        print('team does not have a type')
        data[team['id']] = {'members': team['members']}
    with open('teams.json', 'w') as file:
        json.dump(data, file)


def clear_teams():
    with open('teams.json', 'w') as file:
        json.dump({}, file)


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def split_teams(mixed_teams=True):
    clear_teams()
    # To get data about students
    data_it_d = get_data('it')
    data_nonit_d = get_data('nonit')

    data_it = []
    data_nonit = []

    for i in data_it_d:
        data_it.append(i)

    for i in data_nonit_d:
        data_nonit.append(i)

    if mixed_teams:
        print("creating mixed teams")
        id = 0
        # creating mixed teams
        while len(data_it) > 2 and len(data_nonit) > 2:
            it_part = random.sample(data_it, 2)
            nonit_part = random.sample(data_nonit, 2)

            for i in it_part:
                data_it.remove(i)

            for i in nonit_part:
                data_nonit.remove(i)

            team = {'id': id, 'members': it_part + nonit_part}

            print("added team: ", team)

            add_team(team)

            id += 1

        if len(data_it) > 0 or len(data_nonit) > 0:
            team = {'id': id, 'members': data_it + data_nonit}

            print("added team: ", team)

            add_team(team)

    else:

        print("creating single teams")

        # creating it teams
        id = 0

        while len(data_it) > 2:
            it_part = random.sample(data_it, 4)

            for i in it_part:
                data_it.remove(i)

            team = {'id': id, 'type': 'it', 'members': it_part}

            print("added team: ", team)

            add_team(team)

            id += 1

        if len(data_it) > 0:
            print("some it students left: ", data_it)
            team = {'id': id, 'type': 'it', 'members': data_it}

            print("added team: ", team)
            add_team(team)

        # creating non-it teams
        id = 0

        while len(data_nonit) > 2:
            nonit_part = random.sample(data_nonit, 4)

            for i in nonit_part:
                data_nonit.remove(i)

            team = {'id': id, 'type': 'nonit', 'members': nonit_part}

            print("added team: ", team)

            add_team(team)

            id += 1

        if len(data_nonit) > 0:
            print("some nonit students left: ", data_it)
            team = {'id': id, 'type': 'nonit', 'members': data_nonit}
