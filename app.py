import configparser
import json
import os
from flask import Flask, request
from RedisConnection import connect

app = Flask(__name__)

listen = True
redisCheckThread = None
stack = []
forPublish = {}
minLength = 0
startPoint = 0
r = connect()
@app.route('/Bulker/AddBar',methods=['POST'])
def AddBar():
    newBar = request.json
    stack.append(newBar)
    print("Got new bar: "+str(json.dumps(newBar)))
    GenerateBulks()
    return ""

def GenerateBulks():
    if len(stack) >= lst[0][1]:
        for idx in range(lst[0][1], lst[-1][1]+1):
            if (len(stack)-idx) >= 0:
                forPublish["Bars"] = stack[len(stack)-idx:len(stack)]
                r.lpush(configDef['publishOn'], json.dumps(forPublish))
            else:
                break


def GenerateBulksOLD():
    global stack, r, minLength
    forPublish["from"] = 0
    stackLength = len(stack)
    print("Length of the stack: " + str(stackLength) + "\n")

    if minLength == 0:
        minLength = lst[0][1]
    maxLength = lst[-1][1]
    if stackLength > maxLength:
        print("Delete: "+str(len(stack)))
        del stack[0:1]
        print("Length of the stack after delete: " + str(stackLength) + "\n")
        minLength = 0
    if len(stack) >= minLength:
        for index in range(minLength, stackLength+1):
            if index<0:
                pass
            forPublish["To"] = index
            forPublish["Bars"] = stack[0:index+1]
            print("From: " + str(stack[0]) + " To: " + str(index))
            r.lpush(configDef['publishOn'], json.dumps(forPublish))
        minLength = minLength + 1

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
    app.run(debug=False)