import configparser
import datetime
import json
import threading
from flask import Flask, request
from RedisConnection import connect

app = Flask(__name__)
redisCheckThread = None
stack = []
forPublish = {}
temp = None
lastEnter = None
r = connect()
p = r.pubsub()
p.subscribe("trade")

@app.route('/Bulker/AddBar',methods=['POST'])
def AddBar():
    global rc, lastEnter
    newBar = request.json
    r.publish("newBars", json.dumps(newBar))

    rc = RedisCheck()
    rc.start()

    stack.append(newBar)
    print("Got new bar: " + str(json.dumps(newBar)))

    GenerateBulks()

    while rc.msg is None:
        pass
    temp = rc.msg
    rc.msg = None
    return temp

class RedisCheck(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.msg = None
    def run(self):
        while True:
            currentMessage = p.get_message()
            if currentMessage is not None:
                currentMessage = currentMessage['data']
                if type(currentMessage) == bytes:
                    self.msg = currentMessage.decode("utf-8")
                    if self.msg is not None:
                        break


def GenerateBulks():
    global stack, rc
    if len(stack) >= lst[0][1]:
        for idx in range(lst[0][1], lst[-1][1]+1):
            if (len(stack)-idx) >= 0:
                forPublish["Bars"] = stack[len(stack)-idx:len(stack)]
                firstDate = datetime.datetime.strptime(forPublish["Bars"][0]["date"], '%Y-%m-%d %H:%M:%S')
                lastDate = datetime.datetime.strptime(forPublish["Bars"][-1]["date"], '%Y-%m-%d %H:%M:%S')

                if (((lastDate-firstDate).seconds)/300)+1 != len(forPublish["Bars"]):
                    break

                forPublish["Last"] = False
                if firstDate.date() == lastDate.date():
                    r.rpush(configDef['publishOn'], json.dumps(forPublish))
            else:
                break
    forPublish["Bars"] = []
    forPublish["Last"] = True
    r.rpush(configDef['publishOn'], json.dumps(forPublish))

    #Remove the first element on the bar stack
    if len(stack) > lst[-1][1]:
        stack = stack[1:len(stack)]

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
    #app.config['SERVER_NAME'] = os.getenv("Bulker_HOST")
    app.run(debug=False, host='0.0.0.0')