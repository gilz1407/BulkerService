import os
import sys
import time

lst = [-1,0,0,0,1,2,2,2,2,2,3,4,5,5,5,5,5,5,6,7,8,9,10,11,11,11,11,11,11]
lenMap={}
prevItem = -1
temp = lst[:]
counter = 0
sumFromLst = 0
while len(temp) > 0:
    citem = temp.pop()
    if prevItem != citem:
        if prevItem != -1:
            sumFromLst += counter+1
            lenMap[prevItem] = len(lst)-sumFromLst
        prevItem = citem
        counter = 0
    else:
        counter += 1









lst=lst[2:len(lst)]
def Calc(calc):
    return 7
start = time.time()
func=eval("Calc([2,'4'])<Calc([5,'7'])")
end = time.time()
print(str(start)+"\n")
print(str(end))
print(str(end - start) +"\n")

c = compile("Calc([2,'4'])<Calc([5,'7'])", '<string>', 'eval')

start = time.time()
func=eval(c)
end = time.time()
print(str(end - start))

