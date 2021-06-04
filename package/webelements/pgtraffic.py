import numpy as np
from functools import reduce
import math

def stylecolor(d):
	colors = [[],
			[0x2e, 0xc7, 0xc9],
			[0xb6, 0xa2, 0xde],
			[0x5a, 0xb1, 0xef],
			[0xff, 0xb9, 0x80],
			[0xd8, 0x7a, 0x80],
			[0x8d, 0x98, 0xb3],
			[0xe5, 0xcf, 0x0d],
			[0x97, 0xb5, 0x52]]
	return colors[d]

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

def pgtraffic(data, dataid):
	tid = data.get_tid(dataid)
	pgtraffic_data = data.get_pgtraffic_data(tid)
	data_attr = pgtraffic_data['data_attr']
	elephant_flows = pgtraffic_data['elephant_flows']
	client_statistics = pgtraffic_data['client_statistics']

	heavy_flow = [[0 for i in range(9)] for j in range(9)]
	heavy_traffic = [[0 for i in range(9)] for j in range(9)]
	for item in elephant_flows:
		heavy_flow[item[2]][0] += 1
		heavy_traffic[item[2]][0] += item[6]
		heavy_flow[item[2]][item[1]] += 1
		heavy_traffic[item[2]][item[1]] += item[6]

	flow = [0 for i in range(9)]
	traffic = [0 for i in range(9)]

	flow[0] = data_attr[2]
	traffic[0] = data_attr[3]
	for item in client_statistics:
		flow[item[0]] = item[1]
		traffic[item[0]] = item[2]

	ch_sunburst = []
	for i in range(1, 9):
		datai = {}
		datai['name'] = 'Client ' + str(i)
		datai['value'] = traffic[i]
		datai['children'] = []
		datai['traffic'] = traffic[i]
		datai['flow'] = flow[i]
		heavy = {}
		heavy['name'] = '大象流'
		heavy['itemStyle'] = { 'color': getcolor(0.8, stylecolor(i)) }
		heavy['children'] = []
		heavy['traffic'] = heavy_traffic[i][0]
		heavy['flow'] = heavy_flow[i][0]
		for j in range(1, 9):
			heavy['children'].append({
				'name': 'Client ' + str(j),
				'value': heavy_traffic[i][j],
				'itemStyle': { 'color': getcolor(heavy_traffic[i][j]/max(heavy_traffic[i][1:9])*0.7, stylecolor(i)) },
				'traffic': heavy_traffic[i][j],
				'flow': heavy_flow[i][j]
				})
		datai['children'].append(heavy)
		light = {}
		light['name'] = '鼠流'
		light['traffic'] = traffic[i] - heavy_traffic[i][0]
		light['flow'] = flow[i] - heavy_flow[i][0]
		light['nodeClick'] = 'false'
		light['itemStyle'] = { 'color': getcolor(0.3, stylecolor(i)) }
		light['children'] = [{
			'name': 'Unknown',
			'value': traffic[i] - heavy_traffic[i][0],
			'traffic': traffic[i] - heavy_traffic[i][0],
			'flow': flow[i] - heavy_flow[i][0],
			'itemStyle': { 'color': getcolor(0.3, stylecolor(i)) }
			}]
		datai['children'].append(light)
		ch_sunburst.append(datai)

	maxtraffic = max(1, max([max(i[1:9]) for i in heavy_traffic[1:9]]))

	ch_heatmap = []
	for i in range(1, 9):
		for j in range(1, 9):
			ch_heatmap.append({
				'value': ['Client ' + str(i), 'Client ' + str(j),
					round(heavy_traffic[i][j] / maxtraffic * 100)],
				'itemStyle': { 'color': getcolor(max((heavy_traffic[i][j] / maxtraffic - 0.5) * 2, 0),
					[191,68,76], [240, 217, 156]) }
				})

	basevalue = lambda x : max(math.ceil(math.log10(x + 1) - 2), 0)

	t1 = basevalue(data_attr[2])
	ch_gauge1 = [round(data_attr[2] / 10 ** t1, 2), 10 ** t1]
	t2 = basevalue(data_attr[3])
	ch_gauge2 = [round(data_attr[3] / 10 ** t2, 2), 10 ** t2]

	return { 'ch_sunburst': ch_sunburst, 'ch_heatmap': ch_heatmap,
		'ch_gauge1' : ch_gauge1, 'ch_gauge2' : ch_gauge2 }
