import json
import os
import sys
import threading
import time
from flask import Flask, request
sys.path.append(os.path.abspath('../CrossInfra'))
from Combination import Combination
from RedisManager import connect
app = Flask(__name__)

listen = True
redisCheckThread = None
stack = []
comb = Combination()
forPublish = {}
minLength = 0
r = connect()
@app.route('/Bulker/AddBar',methods=['POST'])
def AddBar():
    print("##############################################")
    print("minLength: "+str(minLength))
    newBar = request.json
    stack.append(newBar)
    print(str(json.dumps(newBar)))
    GenerateBulks()
    print("##############################################")
    return ""


def GenerateBulks():
    global comb, stack, r, minLength
    forPublish["from"] = 0
    stackLength = len(stack)
    print("Length of the stack: " + str(stackLength) + "\n")
    comb.InitCombinations()
    lst = comb.GetCombinationLst()
    if minLength == 0:
        minLength = lst[0][2]
    maxLength = lst[-1][2]
    if stackLength > maxLength:
        print("Delete: "+str(len(stack)))

        del stack[0:1]
        print("Length of the stack after delete: " + str(stackLength) + "\n")
        minLength = minLength = lst[0][2]
        print("MinLength after delete: " + str(minLength))
    if stackLength >= minLength:
        print("First element on stack: "+str(stack[0]))
        for index in range(minLength, stackLength+1):
            forPublish["To"] = index
            forPublish["Bars"] = stack[0:stackLength+1]
            print("To: "+str(index))

            #print("Bars: "+str(stack[0:stackLength]))
            r.lpush('TemplateList', json.dumps(forPublish))
        minLength = minLength + 1
        print("MinLength: " + str(minLength))





@app.route('/Bulker/Start',methods=['POST'])
def StartListen():
    global redisCheckThread
    if redisCheckThread is None:
        listen = True
        redisCheckThread = RedisCheck()
        redisCheckThread.start()
        return "Listening started"
    else:
        return "Already listening"

@app.route('/Bulker/Stop/',methods=['POST'])
def StopListen():
    global listen
    listen = False
    return "Listening stopped"



class RedisCheck(threading.Thread):
    global listen
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        r = connect()  # Connect to local Redis instance
        p = r.pubsub()
        p.subscribe('Bars')  # Subscribe to Bars channel

        while listen:  # Will stay in loop until START message received
            print("Waiting For redisStarter...")
            message = p.get_message()  # Checks for message
            if message:
                command = message['data']  # Get data from message
                bar_json = command.decode('utf8').replace("'", '"')
                Selector().FindSuitablePattern(bar_json)
                print("received: " + str(command))  # Breaks loop

            time.sleep(1)
if __name__ == '__main__':
    app.config['SERVER_NAME'] = "http://127.0.0.1:5555/"
    app.run(debug=True)

#app.config['SERVER_NAME'] = "http://127.0.0.1:5555/"
#app.run(debug=True)
