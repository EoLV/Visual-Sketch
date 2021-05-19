import requests
import json
import sys
import random
import time

def getlen(t):
	if t < 0.15:
		return random.randint(1, 10000)
	if t < 0.2:
		return random.randint(10000, 20000)
	if t < 0.3:
		return random.randint(20000, 30000)
	if t < 0.4:
		return random.randint(30000, 50000)
	if t < 0.53:
		return random.randint(50000, 80000)
	if t < 0.6:
		return random.randint(80000, 200000)
	if t < 0.7:
		return random.randint(20000, 1000000)
	if t < 0.8:
		return random.randint(100000, 2000000)
	if t < 0.9:
		return random.randint(200000, 5000000)
	if t < 0.97:
		return random.randint(500000, 10000000)
	return random.randint(1000000, 30000000)

def getdata(myid):
	ret = {'ID': myid,
		'Algorithm': 'elastic',
		'Time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
		'Cardinality': random.randint(100000, 200000),
		'Entropy': random.uniform(0, 10000)}
	heavypart = []
	distribution = []
	for c in range(8):
		td = {}
		for i in range(50000 + c + 1):
			pktnum = getlen(random.random()) // 1460 + 1
			if pktnum > 500:
				pktnum = pktnum // 100 * 100 + 100
			if len(heavypart) < 1000 and pktnum > 1000:
				heavypart.append([
					3232235777 + random.randint(0, 7),
					random.randint(3000, 6000),
					3232235777 + random.randint(0, 7),
					random.randint(3000, 6000),
					"TCP",
					pktnum,
					0 if random.random() < 0.7 else 1])
			if not pktnum in td:
				td[pktnum] = 1
			else:
				td[pktnum] = td[pktnum] + 1
		distribution.append(td)
	ret['HeavyPart'] = heavypart
	ret['Distribution'] = distribution
	return ret

url = "http://localhost:5001/post"

aheaders = { 'Content-Type' : 'application/json' }


for i in range(100, 105):
	print('start %d' %i)
	datajson = json.dumps(getdata(i))
	print(datajson)
	print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	response = requests.post(url, headers=aheaders, data = datajson)
	print(response.text)

