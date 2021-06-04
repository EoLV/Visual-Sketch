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

def pgelephant(data, dataid):
	tid = data.get_tid(dataid)
	# [[fid, src, dst, src_port, dst_port, protocol, size, increment]]
	pgelephant_data = data.get_pgelephant_data(tid)

	pgelephant_data = sorted(pgelephant_data, key=lambda x: x[6], reverse=True)
	ch_allflow = []
	for item in pgelephant_data:
		now = {
			'name': 'Client ' + str(item[2]),
			'value': [len(ch_allflow) + 1, item[6]],
			'ID': item[0],
			'itemStyle': {
				'color': getcolor(1, stylecolor(item[2])),
			}
		}
		if item[7]:
			now['itemStyle']['borderColor'] = getcolor(0.5, stylecolor(item[2]))
			now['itemStyle']['borderWidth'] = 2
		ch_allflow.append(now)
	ch_active = []
	pgelephant_data = sorted(pgelephant_data, key=lambda x: x[7], reverse=True)
	for item in pgelephant_data:
		if not item[7]:
			continue
		now = {
			'name': 'Client ' + str(item[2]),
			'value': [len(ch_active) + 1, item[6]],
			'ID': item[0],
			'itemStyle': {
				'color': getcolor(1, stylecolor(item[2])),
			}
		}
		if item[7]:
			now['itemStyle']['borderColor'] = getcolor(0.5, stylecolor(item[2]))
			now['itemStyle']['borderWidth'] = 2
		ch_active.append(now)

	return { 'ch_allflow': ch_allflow, 'ch_active': ch_active }
