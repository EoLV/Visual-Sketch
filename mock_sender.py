import requests
import json
import sys
import random
import time
from functools import reduce

def getlen(t):
	if t < 0.15:
		return random.randint(1, 10000) // 1460 + random.randint(0, 1)
	if t < 0.2:
		return random.randint(10000, 20000) // 1460 + random.randint(0, 1)
	if t < 0.3:
		return random.randint(20000, 30000) // 1460 + random.randint(0, 1)
	if t < 0.4:
		return random.randint(30000, 50000) // 1460 + random.randint(0, 1)
	if t < 0.53:
		return random.randint(50000, 80000) // 1460 + random.randint(0, 1)
	if t < 0.6:
		return random.randint(80000, 200000) // 1460 + random.randint(0, 1)
	if t < 0.7:
		return random.randint(200000, 1000000) // 1460 + random.randint(0, 1)
	if t < 0.8:
		return random.randint(100000, 2000000) // 1460 + random.randint(0, 1)
	if t < 0.9:
		return random.randint(200000, 5000000) // 1460 + random.randint(0, 1)
	if t < 0.97:
		return random.randint(500000, 10000000) // 1460 + random.randint(0, 1)
	return random.randint(1000000, 30000000) // 1460 + random.randint(0, 1)

convert_endian = lambda x: reduce(lambda a, b: a + b, [x//(256**i)%256*(256**(3-i)) for i in range(3,-1,-1)][::-1])

flows = {}

def getdata(myid):
	data = {'ID': myid,
		'Algorithm': 'elastic',
		'Time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
		'Cardinality': random.randint(100000, 200000),
		'Entropy': random.uniform(0, 10000)}
	for i in range(100):
		pktnum = getlen(random.random())
		if pktnum > 500:
			pktnum = pktnum // 100 * 100 + 100
		fivetuple = (3232235778 + random.randint(0, 7), 3232235778 + random.randint(0, 7),
					random.randint(3000, 3010), random.randint(3000, 3010), "TCP")
		if fivetuple not in flows:
			flows[fivetuple] = pktnum
		flows[fivetuple] += pktnum

	heavypart = []
	distribution = [{} for i in range(8)]
	for (fivetuple, fsize) in flows.items():
		if fsize not in distribution[fivetuple[1] - 3232235778]:
			distribution[fivetuple[1] - 3232235778][fsize] = 1
		else:
			distribution[fivetuple[1] - 3232235778][fsize] += 1
		if fsize > 20:
			heavypart.append([convert_endian(fivetuple[0]), convert_endian(fivetuple[1]), fivetuple[2], fivetuple[3], fivetuple[4], fsize, 0])
	data['HeavyPart'] = heavypart
	data['Distribution'] = [list(distribution[i].items()) for i in range(8)]
	return data

url = "http://localhost:5001/post"

aheaders = { 'Content-Type' : 'application/json' }


response = requests.get("http://localhost:5001/clean")
print(response.text)

for i in range(1, 20):
	print('start %d' %i)
	datajson = json.dumps(getdata(i))
	# print(datajson)
	print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	response = requests.post(url, headers=aheaders, data = datajson)
	print(response.text)

