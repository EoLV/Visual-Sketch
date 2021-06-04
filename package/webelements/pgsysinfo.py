def pgsysinfo(data, dataid):
	tid = data.get_tid(dataid)
	# [[fid, src, dst, src_port, dst_port, protocol, size, increment]]
	pgsysinfo_data = data.get_pgsysinfo_data(tid)
	sys_info = pgsysinfo_data['sys_info']
	data_time = pgsysinfo_data['time']
	clients = pgsysinfo_data['clients']

	sys_status = sys_info[0]
	start_time = sys_info[1]

	tb_client = []
	for item in clients:
		t = []
		t.append('<tr>')
		t.append('<td>' + str(item[0]) + '</td>')
		t.append('<td>' + str(item[1]) + '</td>')
		t.append('<td>' + str(item[2]) + '</td>')
		t.append('<td>' + str(item[3]) + '</td>')
		t.append('</tr>')
		tb_client.append("".join(t))

	return {'sys_status': sys_status, 'start_time': start_time, 'data_time': data_time, 'tb_client': tb_client}
