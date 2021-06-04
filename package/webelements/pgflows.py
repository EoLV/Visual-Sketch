int_to_ip = lambda x: '.'.join([str(x//(256**i)%256) for i in range(3,-1,-1)])

def pgflows(data, dataid):
	tid = data.get_tid(dataid)
	# [[fid, src, dst, src_port, dst_port, protocol, size, increment]]
	pgflows_data = data.get_pgflows_data(tid)
	result = []
	for item in pgflows_data:
		t = []
		t.append('<tr>')
		t.append('<td>' + str(item[0]) + '</td>')
		t.append('<td>' + str(item[1]) + '</td>')
		t.append('<td>' + str(int_to_ip(data.get_client_addr(item[1]))) + '</td>')
		t.append('<td>' + str(item[3]) + '</td>')
		t.append('<td>' + str(item[2]) + '</td>')
		t.append('<td>' + str(int_to_ip(data.get_client_addr(item[2]))) + '</td>')
		t.append('<td>' + str(item[4]) + '</td>')
		t.append('<td>' + str(item[5]) + '</td>')
		t.append('<td>' + str(item[6]) + '</td>')
		t.append('</tr>')
		result.append("".join(t))
	return result

