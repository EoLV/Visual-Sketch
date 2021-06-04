import math

def pgdistri(data, dataid):
	tid = data.get_tid(dataid)
	pgdistri_data = data.get_pgdistri_data(tid)

	data_attr = pgdistri_data['data_attr']
	distribution = pgdistri_data['distribution']
	client_statistics = pgdistri_data['client_statistics']
	maxsize = pgdistri_data['maxsize']
	# 主机的数量8个在这里暂时写死了，如果需要修改
	# 由于每一个主机对应一条折线，大概折线图的整个series都要用代码生成再传进去
	legend = ['Client' + str(i) for i in range(1, 9)]

	base = 10 ** max(0, math.ceil(math.log10(maxsize) - 3))
	xaxisdata = [i * base for i in range(maxsize // base + 2)]
	mouse_xaxisdata = [i for i in range(501)]

	flow_all = [[0.6 for i in range(maxsize // base + 2)] for j in range(9)]
	traffic_all = [[0 for i in range(maxsize // base + 2)] for j in range(9)]

	flow_mouse = [[0.6 for i in range(501)] for j in range(9)]
	traffic_mouse = [[0 for i in range(501)] for j in range(9)]

	divpoint = [20, 50, 200, 500, 2000, 1e20]
	pielabels = ['≤20', '≤50', '≤200', '≤500', '≤2K', '>2K']
	flow_pie = [[{'name': pielabels[i], 'value': 0} for i in range(6)] for j in range(9)]
	traffic_pie = [[{'name': pielabels[i], 'value': 0} for i in range(6)] for j in range(9)]

	for item in distribution:
		client = item[0]
		size = item[1]
		count = item[2]

		flow_all[client][(size - 1) // base + 1] += count
		traffic_all[client][(size - 1) // base + 1] += size * count

		if size <= 500:
			flow_mouse[client][size] += count
			traffic_mouse[client][size] += size * count

		for i in range(6):
			if size < divpoint[i]:
				flow_pie[0][i]['value'] += count
				traffic_pie[0][i]['value'] += size * count
				flow_pie[client][i]['value'] += count
				traffic_pie[client][i]['value'] += size * count
				break

	flow_detail = [0 for i in range(9)]
	traffic_detail = [0 for i in range(9)]
	entropy_detail = [0 for i in range(9)]

	flow_detail[0] = data_attr[2]
	traffic_detail[0] = data_attr[3]
	entropy_detail[0] = data_attr[4]
	for item in client_statistics:
		flow_detail[item[0]] = item[1]
		traffic_detail[item[0]] = item[2]
		entropy_detail[item[0]] = item[3]

	return {
		'xaxisdata': xaxisdata,
		'flow_all': flow_all,
		'traffic_all': traffic_all,
		'mouse_xaxisdata': mouse_xaxisdata,
		'flow_mouse': flow_mouse,
		'traffic_mouse': traffic_mouse,
		'flow_pie': flow_pie,
		'traffic_pie': traffic_pie,
		'flow_detail': flow_detail,
		'traffic_detail': traffic_detail,
		'entropy_detail': entropy_detail
	}


