#!/usr/bin/python
# -*- coding: <encoding name> -*-

import json
import threading
import win32com.client as comclt
from time import sleep
from flask import Flask, request, jsonify
from threading import Thread

from settings import HOST, PORT
from responses import InvalidUsage
import keys
from keys import KEY


def input_queue_thread(queue):
    for item in queue:
        wait = item.get('wait', 0)
        action = item.get('action', 'press')
        duration = item.get('duration', 0.05)
        key = KEY.get(item.get('key'))

        if item.get('wait'):
            sleep(wait)

        if key is None:
            return

        if action == 'press':
            keys.press(key, duration=duration)
        if action == 'down':
            keys.down(key)
        if action == 'up':
            keys.up(key)

    return


app = Flask(__name__)

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route("/input/queue", methods=['POST'])
def queue():
    input_raw = request.get_data()
    try:
        input_json = json.loads(input_raw.decode('utf-8'))
    except Exception as e:
        raise InvalidUsage('Invalid JSON POST data supplied {} [{}]'.format(e, input_raw))

    commands = input_json.get('commands')
    if not commands or not type(commands) is list:
        raise InvalidUsage('Invalid commands list specified')

    thread = Thread(target=input_queue_thread, args=(commands,))
    thread.start()

    return jsonify({ "success": True })


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)