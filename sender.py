import requests
import json
import sys
import random
import time

url = "http://localhost:5001/post"

aheaders = { 'Content-Type' : 'application/json' }

filename = '1621534952_3528554'

with open(filename) as f:
	data = json.load(f)

print('start %s' %filename)
datajson = json.dumps(data)
# print(datajson)
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
response = requests.post(url, headers=aheaders, data = datajson)
print(response.text)

