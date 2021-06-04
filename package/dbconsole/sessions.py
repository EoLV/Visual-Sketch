import sqlalchemy
from sqlalchemy import text
import traceback

def dbinsert(session, model, item):
	try:
		if model.__tablename__ == 'sys_info':
			row = model(status = item[0], start_time = item[1], source_addr = item[2],
				source_port = item[3], source_agent = item[4])
			result = session.add(row)
		if model.__tablename__ == 'data_info':
			row = model(tid = item[0], time = item[1], data_type = item[2],
				flow_count = item[3], traffic_count = item[4], entropy = item[5], deleted = item[6])
			result = session.add(row)
		if model.__tablename__ == 'clients':
			row = model(cid = item[0], addr = item[1])
			result = session.add(row)
		if model.__tablename__ == 'flows':
			row = model(fid = item[0], src = item[1], dst = item[2],
				src_port = item[3], dst_port = item[4], protocol = item[5])
			result = session.add(row)
		session.commit()
	except:
		traceback.print_exc()
		return 'insert error'
	return 'accepted'

def dbinsert_all(session, model, items):
	try:
		s = ''
		if model.__tablename__ == 'distribution':
			s = 'INSERT INTO distribution (tid, cid, size, count) VALUES '
		if model.__tablename__ == 'client_statistics':
			s = 'INSERT INTO client_statistics (tid, cid, flow_count, traffic_count, entropy) VALUES '
		if model.__tablename__ == 'elephant_flows':
			s = 'INSERT INTO elephant_flows (tid, fid, size, increment) VALUES '
		if model.__tablename__ == 'clients':
			s = 'INSERT INTO clients (cid, addr) VALUES '
		if model.__tablename__ == 'flows':
			s = 'INSERT INTO flows (fid, src, dst, src_port, dst_port, protocol) VALUES '

		cmd = [s]
		item_cnt = 0
		for item in items:
			item_cnt += 1
			if item_cnt > 1:
				cmd.append(',')
			cmd.append('(' + ','.join(list(map(lambda x: '"' + str(x) + '"', item))) + ')')
			# 若SQL语句过长会产生错误
			if item_cnt > 10000:
				session.execute(text(''.join(cmd)))
				cmd = [s]
				item_cnt = 0
		if item_cnt > 0:
			session.execute(text(''.join(cmd)))
		session.commit()
	except:
		# traceback.print_exc()
		return 'insert error'
	return 'accepted'

def dbdelete(session, model, order = '', desc = False, limit = '', where = ''):
	res = []
	try:
		cmd = 'DELETE FROM %s' %model.__tablename__
		if order:
			cmd += ' ORDER BY ' + str(order)
		if desc:
			cmd += ' DESC '
		if limit:
			cmd += ' LIMIT ' + str(limit)
		if where:
			cmd += ' WHERE ' + str(where)
		session.execute(text(cmd))
		session.commit()
	except:
		# traceback.print_exc()
		return 'delete error'
	return 'accepted'

def dbselect(session, model, field = '*', order = '', desc = False, limit = '', where = ''):
	res = []
	try:
		cmd = 'SELECT %s FROM %s' %(field, model.__tablename__)
		if order:
			cmd += ' ORDER BY ' + str(order)
		if desc:
			cmd += ' DESC '
		if limit:
			cmd += ' LIMIT ' + str(limit)
		if where:
			cmd += ' WHERE ' + str(where)
		t = session.execute(text(cmd))
		for row in t:
			res.append(list(row))
	except:
		traceback.print_exc()
		pass
	return res

def dbcommand(session, command):
	res = []
	try:
		t = session.execute(text(command))
		session.commit()
		for row in t:
			res.append(list(row))
	except:
		pass
	return res
