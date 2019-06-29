import requests

def streamBars():
    open = 1
    close = 1
    min = 1
    max = 1
    while open<37:
        requests.post('http://127.0.0.1:7000/Bulker/AddBar',json={"open":open,"close":close,"min":min,"max":max})
        open = open + 1
        close = close + 1
        min = min + 1
        max = max + 1

streamBars()

