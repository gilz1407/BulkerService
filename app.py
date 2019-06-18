import configparser
import json
import os
import sys
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

            r.lpush('TemplateList', json.dumps(forPublish))
        minLength = minLength + 1
        print("MinLength: " + str(minLength))


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    configDef = config['DEFAULT']
    app.config['SERVER_NAME'] = configDef['url']
    app.run(debug=True)