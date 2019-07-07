#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request
import json

from manager import Manager
from interfaces import api_mapping
from mappings import users

app = Flask('tamagochi')


@app.route("/", methods=['POST'])
def api():
    try:
        rjs = request.get_json(force=True)

        method = rjs['functionName']
        if method == 'register':
            response = json.dumps({"uuid": Manager.register_user()}, ensure_ascii=False)
            from scenario import Scenario
            Scenario.test_curcit()
            return response
        guid = rjs['uuid']
        data = rjs['data']

        client = users[guid]
        response = api_mapping[method](client, data)

    except Exception as e:
        if hasattr(e, 'name'):
            return json.dumps({
                "status": False,
                "message": e.name,
                "response": None
            })
        raise e

    return json.dumps({
                "status": True,
                "message": "Всё ОК",
                "response": response
            }, ensure_ascii=False)


if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)
