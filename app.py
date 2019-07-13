import configparser
import json
import os
import threading
from flask import Flask, request
from RedisConnection import connect

app = Flask(__name__)
rc = None
redisCheckThread = None
stack = []
forPublish = {}
r = connect()

@app.route('/Bulker/Hello',methods=['GET'])
def hello():
    return "Hello World"

@app.route('/Bulker/AddBar',methods=['POST'])
def AddBar():
    print("Hello")
    global rc
    rc = RedisCheck()
    newBar = request.json
    stack.append(newBar)
    print("Got new bar: "+str(json.dumps(newBar)))
    rc.start()
    GenerateBulks()
    return rc.msg

class RedisCheck(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.msg = None
    def run(self):
        p = r.pubsub()
        p.subscribe("trade")
        while True:
            currentMessage = p.get_message()
            if currentMessage is not None:
                currentMessage = currentMessage['data']
                if type(currentMessage) == bytes:
                    self.msg = currentMessage.decode("utf-8")
                    break

def GenerateBulks():
    global stack, rc
    if len(stack) >= lst[0][1]:
        for idx in range(lst[0][1], lst[-1][1]+1):
            if rc.msg is not None:
                break
            if (len(stack)-idx) >= 0:
                forPublish["Bars"] = stack[len(stack)-idx:len(stack)]
                forPublish["Last"] = False
                r.rpush(configDef['publishOn'], json.dumps(forPublish))
            else:
                break
    forPublish["Bars"] = []
    forPublish["Last"] = True
    r.rpush(configDef['publishOn'], json.dumps(forPublish))
    while rc.msg is None:
        pass


    #Remove the first element on the bar stack
    if len(stack) > lst[-1][1]:
        stack = stack[1:len(stack)]

    while rc.msg is None:
        pass

if __name__ == '__main__':
    # load combination list from redis
    combLst = r.get("tempComb")
    l = json.loads(combLst)
    lst = eval(l['tl'])
    global configDef

    config = configparser.ConfigParser()
    config.read('config.ini')
    configDef = config['DEFAULT']
    r.delete(configDef['publishOn'])
    app.config['SERVER_NAME'] = os.getenv("Bulker_HOST")
    print("Before app run")
    app.run(debug=False)