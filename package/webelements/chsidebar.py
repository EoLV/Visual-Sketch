def chsidebar(data, dataid):
	tid = data.get_tid(dataid)
	data_info = data.get_data_info()

	ch_sidebar = []
	for i in sorted(data_info.keys(), reverse=True):
		now = {
			'name': data_info[i][0],
			'value': [i, data_info[i][2]],
			'time': data_info[i][1],
			'itemStyle': {
				'color': "#759aa0",
			}
		}
		ch_sidebar.append(now)
	return { 'dataid': tid, 'ch_sidebar': ch_sidebar }
