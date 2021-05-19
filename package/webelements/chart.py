import numpy as np
from functools import reduce
import math

def stylecolor(d):
	colors = [
			[0x2e, 0xc7, 0xc9],
			[0xb6, 0xa2, 0xde],
			[0x5a, 0xb1, 0xef],
			[0xff, 0xb9, 0x80],
			[0xd8, 0x7a, 0x80],
			[0x8d, 0x98, 0xb3],
			[0xe5, 0xcf, 0x0d],
			[0x97, 0xb5, 0x52]]
	return colors[d % 8]

def getcolor(ms, end = [0,0,0], start = [255,255,255]):
	if ms < 0:
		ms = 0
	if ms > 1:
		ms = 1
	me = 1 - ms
	res = []
	for i in range(3):
		res.append(int(start[i] * me + end[i] * ms))
	return '#%02x%02x%02x' %(res[0], res[1], res[2])


def distrchart(data, attrid):
	attr = data.attrid()[-attrid]
	f = data.distribution(attr[0])

	xaxisdata = [i * 100 for i in range(0, f[9] + 1)]

	linedata1 = {}
	for i in range(8):
		linedata1['Client '+str(i+1)] = []
		for j in range(0, f[9] + 1):
			linedata1['Client '+str(i+1)].append(max(f[0][i][j], 0.9))

	linedata2 = {}
	for i in range(8):
		linedata2['Client '+str(i+1)] = []
		for j in range(0, f[9] + 1):
			linedata2['Client '+str(i+1)].append(f[1][i][j])

	antxaxisdata = [i for i in range(501)]

	antlinedata1 = {}
	for i in range(8):
		antlinedata1['Client '+str(i+1)] = []
		for j in range(501):
			antlinedata1['Client '+str(i+1)].append(max(f[7][i][j], 0.9))

	antlinedata2 = {}
	for i in range(8):
		antlinedata2['Client '+str(i+1)] = []
		for j in range(501):
			antlinedata2['Client '+str(i+1)].append(f[8][i][j])

	pielabels = ['≤20', '≤100', '≤500', '≤2k', '≤8k', '>8k']
	bind = lambda x, y: [{'name': x[i], 'value': y[i]} for i in range(6)]
	
	piedata1 = {}
	pietotal1 = [0 for i in range(6)]
	for i in range(8):
		piedata1['Client '+str(i+1)] = bind(pielabels, f[2][i])
		for j in range(6):
			pietotal1[j] += f[2][i][j]
	piedata1['total'] = bind(pielabels, pietotal1)

	piedata2 = {}
	pietotal2 = [0 for i in range(6)]
	for i in range(8):
		piedata2['Client '+str(i+1)] = bind(pielabels, f[3][i])
		for j in range(6):
			pietotal2[j] += f[3][i][j]
	piedata2['total'] = bind(pielabels, pietotal2)


	flowall = f[4].copy()
	flowall.append(reduce(lambda x, y: x + y, f[4]))

	pktall = f[5].copy()
	pktall.append(reduce(lambda x, y: x + y, f[5]))

	maxvalue = lambda x : math.ceil(math.log10(x + 1) - 2)

	entropy = f[6].copy()
	entropy.append(float(attr[3]))
	entropy = list(map(lambda x: [round(x / 10 ** maxvalue(x), 2), 10 ** maxvalue(x)], entropy))

	return {'xaxisdata': xaxisdata, 'linedata1': linedata1, 'linedata2': linedata2,
		'antxaxisdata': antxaxisdata, 'antlinedata1': antlinedata1, 'antlinedata2': antlinedata2, 
		'piedata1': piedata1, 'piedata2': piedata2, 'flowall': flowall, 'pktall': pktall, 'entropy': entropy
		}

def trafficchart(data, attrid):
	attr = data.attrid()[-attrid]
	f = data.traffic(attr[0])

	sunburstdata = []
	for i in range(8):
		datai = {}
		datai['name'] = 'Client ' + str(i + 1)
		datai['value'] = f[2][i]
		datai['children'] = []
		datai['traffic'] = f[2][i]
		datai['flow'] = f[3][i]
		heavysum = reduce(lambda x, y: x + y, f[0][i])
		heavyflowsum = reduce(lambda x, y: x + y, f[1][i])
		heavymax = max(1, reduce(lambda x, y: max(x, y), f[0][i]))
		scale = min(max(heavysum, f[2][i] * 0.7), f[2][i] * 0.8) / max(1, heavysum)
		lightvalue = f[2][i]
		heavy = {}
		heavy['name'] = '大象流'
		heavy['itemStyle'] = { 'color': getcolor(0.8, stylecolor(i)) }
		heavy['children'] = []
		heavy['traffic'] = heavysum
		heavy['flow'] = heavyflowsum
		for j in range(8):
			value = 0
			if f[0][i][j]:
				value = int(max(f[0][i][j] * scale, f[2][i] / 40))
			lightvalue -= value
			heavy['children'].append({
				'name': 'Client ' + str(j + 1),
				'value': value,
				'itemStyle': { 'color': getcolor(f[0][i][j]/heavymax*0.7, stylecolor(i)) },
				'traffic': f[0][i][j],
				'flow': f[1][i][j]
				})
		datai['children'].append(heavy)
		light = {}
		light['name'] = '鼠流'
		light['traffic'] = f[2][i] - heavysum
		light['flow'] = f[3][i] - heavyflowsum
		light['nodeClick'] = 'false'
		light['itemStyle'] = { 'color': getcolor(0.3, stylecolor(i)) }
		light['children'] = [{
			'name': 'Unknown',
			'value': lightvalue,
			'traffic': f[2][i] - heavysum,
			'flow': f[3][i] - heavyflowsum,
			'itemStyle': { 'color': getcolor(0.3, stylecolor(i)) }
			}]
		sunburstdata.append(datai)
		datai['children'].append(light)
	# sunburstdata --datai --heavy --1-8
	#              |       |-light
	#              |-...

	matrixmax = 1
	for i in range(8):
		for j in range(8):
			matrixmax = max(matrixmax, f[0][i][j])
	print(matrixmax)
	print(f[0])
	heatmapdata = []
	for i in range(8):
		for j in range(8):
			heatmapdata.append({
				'value': ['Client ' + str(i + 1), 'Client ' + str(j + 1),
					round(f[0][i][j] / matrixmax * 100)],
				'itemStyle': { 'color': getcolor(max((f[0][i][j] / matrixmax - 0.3) * 1.4, 0),
					[191,68,76], [240, 217, 156]) }
				})
	print(heatmapdata)

	maxvalue = lambda x : math.ceil(math.log10(x + 1) - 2)

	t1 = maxvalue(f[4])
	gauge1data = [round(f[4] / 10 ** t1, 2), 10 ** (t1 - 6)]
	t2 = maxvalue(f[5])
	gauge2data = [round(f[5] / 10 ** t2, 2), 10 ** t2]

	return { 'sunburstdata': sunburstdata, 'heatmapdata': heatmapdata,
		'gauge1data' : gauge1data, 'gauge2data' : gauge2data }

def elephantchart(data, attrid):
	attr = data.attrid()[-attrid]
	f = data.allflow(attr[0])

	f = sorted(f, key=lambda x: x[5], reverse=True)
	elephantdata = []
	for i in f:
		now = {
			'name': 'Client ' + str((i[2]-1) % 8 + 1),
			'value': [len(elephantdata) + 1, i[5]],
			'ID': i[7],
			'itemStyle': {
				'color': getcolor(1, stylecolor((i[2]-1) % 8)),
			}
		}
		if i[6]:
			now['itemStyle']['borderColor'] = getcolor(0.5, stylecolor((i[2]-1) % 8))
			now['itemStyle']['borderWidth'] = 2
		elephantdata.append(now)
	swaptdata = []
	for i in f:
		if not i[6]:
			continue
		now = {
			'name': 'Client ' + str((i[2]-1) % 8 + 1),
			'value': [len(swaptdata) + 1, i[5]],
			'ID': i[7],
			'itemStyle': {
				'color': getcolor(1, stylecolor((i[2]-1) % 8)),
			}
		}
		now['itemStyle']['borderColor'] = getcolor(0.5, stylecolor((i[2]-1) % 8))
		now['itemStyle']['borderWidth'] = 2
		swaptdata.append(now)

	return { 'elephantdata': elephantdata, 'swaptdata': swaptdata }

def sidebarchart(data, attrid):
	attr = data.attrid()
	n = min(len(attr), 10)
	sidebardata = []
	for i in range(1, n + 1):
		now = {
			'name': attr[-i][0],
			'value': [i, attr[-i][2]],
			'time': attr[-i][1],
			'itemStyle': {
				'color': "#759aa0",
			}
		}
		if i == attrid:
			now['itemStyle']['color'] = "#dd6b66"
			now['itemStyle']['borderColor'] = getcolor(0.5, [0xdd, 0x6b, 0x66])
			now['itemStyle']['borderWidth'] = 2
		sidebardata.append(now)
	return { 'sidebardata': sidebardata, 'thisattr': attr[-attrid] }
