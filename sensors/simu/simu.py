#!/usr/bin/env python

import websocket
import threading
import time
import json
import random

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        while ws.sock :
            obj = {'msg': 'setTemperature', 'temperature' : random.randint(10, 28)}
            ws.send(json.dumps(obj))
            time.sleep(5)
    _threading.start_new_thread(run, ())

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8000/",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
