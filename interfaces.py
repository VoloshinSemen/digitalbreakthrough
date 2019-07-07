import json

from classes import *
from scenario import *

api_mapping = {
    'common': lambda client, params: common(client),
    'mainscreen': lambda client, params: mainscreen(client),
    'mails': lambda client, params: mails(client),
    'mailaction': lambda client, params: mailaction(client, **params),
    'shopaction': lambda client, params: shopaction(client, **params),
    'history': lambda client, params: history(client),
    'run_test_scenario': lambda client, params: run_test_scenario(),
}


def common(client):
    return {
        "name": client.user.name,
        "shop": Shop.response()
    }


def mainscreen(client):
    return client.responce()


def mails(client):
    return client.mailbox.responce()


def mailaction(client, mail, action):
    response = client.mailbox.mails[mail].perform_action(action, client)
    response['state'] = client.responce()
    return response


def shopaction(client, type, id):
    if type == 'buff':
        buff = [buff for buff in Shop.buffs if buff.id == id][0]
        buff.action(client)
    if type == 'offence':
        offense = [offense for offense in Shop.offenses if offense.id == id][0]
        offense.action(client)
    return client.responce()


def history(client):
    return client.history.response()


def run_test_scenario():
    Scenario.test_curcit()
    return {
        "status": True,
        "message": "",
        "response": "OK"
    }
