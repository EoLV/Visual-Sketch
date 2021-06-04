def chflowhis(data, fid):
	# [[tid, time, size]]
	flowhis = data.get_flow_history(fid)

	ch_flowhis = []
	for item in sorted(flowhis, key=lambda x: x[0]):
		now = [item[0], item[2], item[1]]
		ch_flowhis.append(now)
		
	return { 'ch_flowhis': ch_flowhis }
