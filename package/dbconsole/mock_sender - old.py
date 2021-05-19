import requests
import json
import sys
import random
import time

def getdata(myid):
	ret = {'ID': myid,
		'Algorithm': 'elastic',
		'Time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
		'Cardinality': 2,
		'Entropy': random.uniform(0, 10000)}
	heavypart = []
	distribution = []
	for c in range(8):
		td = {}
		for i in range(30000 + c + 1):
			pktnum = random.randint(100, 300000)
			if len(heavypart) < 1000 and pktnum > 298000:
				heavypart.append([
					3232235777 + random.randint(0, 7),
					random.randint(3000, 6000),
					3232235777 + random.randint(0, 7),
					random.randint(3000, 6000),
					"TCP",
					pktnum,
					random.randint(0, 1)])
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


for i in range(100, 110):
	print('start %d' %i)
	datajson = json.dumps(getdata(i))
	print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	response = requests.post(url, headers=aheaders, data = datajson)
	print(response.text)

