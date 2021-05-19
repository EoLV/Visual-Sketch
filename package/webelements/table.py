int_to_ip = lambda x: '.'.join([str(x//(256**i)%256) for i in range(3,-1,-1)])

def flowtable(data, attrid):
	attr = data.attrid()[-attrid]
	f = data.allflow(attr[0])
	s = []
	s.append(
		'<thead><tr><th>ID</th><th>源IP地址</th><th>源端口</th>' \
		'<th>目的IP地址</th><th>目的端口</th><th>传输层协议</th>' \
		'<th>流报文数</th></tr></thead><tbody>')
	for i in f:
		s.append('<tr>')
		s.append('<td>' + str(i[7]) + '</td>')
		s.append('<td>' + int_to_ip(i[0]) + '</td>')
		s.append('<td>' + str(i[1]) + '</td>')
		s.append('<td>' + int_to_ip(i[2]) + '</td>')
		s.append('<td>' + str(i[3]) + '</td>')
		s.append('<td>' + str(i[4]) + '</td>')
		s.append('<td>' + str(i[5]) + '</td>')
		s.append('</tr>')
	s.append('</tbody>')
	return "".join(s)

