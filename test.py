#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import requests
import pprint
from random import randint

pp = pprint.PrettyPrinter(indent=4)

url = 'http://127.0.0.1:8001/'

pp.pprint('Зарегай юзера')
j = json.dumps({'functionName': 'register',
                'uuid': None,
                'data': None,
                })
pp.pprint(j)
r = requests.post(url=url, json=j)
pp.pprint(r.json())

guid = r.json()['uuid']

pp.pprint('Получи основные функции')
j = json.dumps({'functionName': 'common',
                'uuid': guid,
                'data': None,
                })
r = requests.post(url=url, json=j)
pp.pprint(j)
pp.pprint(r.json())

pp.pprint('Получи статусы')
j = json.dumps({'functionName': 'mainscreen',
                'uuid': guid,
                'data': None,
                })
pp.pprint(j)
r = requests.post(url=url, json=j)
pp.pprint(r.json())

pp.pprint('Получи письма')
j = json.dumps({'functionName': 'mails',
                'uuid': guid,
                'data': None,
                })
pp.pprint(j)
r = requests.post(url=url, json=j)
pp.pprint(r.json())

mails = r.json()['response']['mails']
for mail in mails:
    pp.pprint('Ответ на письмо')
    j = json.dumps({'functionName': 'mailaction',
                    'uuid': guid,
                    'data': {
                        "mail": mail['id'],
                        "action": randint(0, 3)
                    },
                    })
    pp.pprint(j)
    r = requests.post(url=url, json=j)
    pp.pprint(r.json())

pp.pprint('Получи письма')
j = json.dumps({'functionName': 'mails',
                'uuid': guid,
                'data': None,
                })
pp.pprint(j)
r = requests.post(url=url, json=j)
pp.pprint(r.json())

pp.pprint('Позови админа')
j = json.dumps({'functionName': 'shopaction',
                'uuid': guid,
                'data': {
                    "type": "buff",
                    "id": 1,
                },
                })
pp.pprint(j)
r = requests.post(url=url, json=j)
pp.pprint(r.json())

pp.pprint('Позови админа')
j = json.dumps({'functionName': 'history',
                'uuid': guid,
                'data': None,
                })
pp.pprint(j)
r = requests.post(url=url, json=j)
pp.pprint(r.json())

pp.pprint('Получи статусы')
j = json.dumps({'functionName': 'mainscreen',
                'uuid': guid,
                'data': None,
                })
pp.pprint(j)
r = requests.post(url=url, json=j)
pp.pprint(r.json())

pp.pprint('Получи статусы')
j = json.dumps({'functionName': 'mainscreen',
                'uuid': guid,
                'data': None,
                })
pp.pprint(j)
r = requests.post(url=url, json=j)
pp.pprint(r.json())

pp.pprint('Рейтинг')
j = json.dumps({'functionName': 'rating',
                'uuid': guid,
                'data': None,
                })
pp.pprint(j)
r = requests.post(url=url, json=j)
pp.pprint(r.json())

pp.pprint('Рейтинг')
j = json.dumps({'functionName': 'rating',
                'uuid': guid,
                'data': None,
                })
pp.pprint(j)
r = requests.post(url=url, json=j)
pp.pprint(r.json())

'''
pp.pprint('Создай письма')
j = json.dumps({'functionName': 'run_test_scenario',
                'uuid': guid,
                'data': None,
                })
pp.pprint(j)
r = requests.post(url=url, json=j)
print(r.text)

pp.pprint('Получи письма')
j = json.dumps({'functionName': 'mails',
                'uuid': guid,
                'data': None,
                })
pp.pprint(j)
r = requests.post(url=url, json=j)
pp.pprint(r.json())
'''
