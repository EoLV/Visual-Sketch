import sqlalchemy
from sqlalchemy import text
import traceback
import time
import json
import sys

def save_elastic_session(session, data, Attribute, Heavypart, Distribution):
	try:
		row = Attribute(ID=data['ID'],
			Algorithm=data['Algorithm'],
			Time=data['Time'],
			Cardinality=data['Cardinality'],
			Entropy=str(data['Entropy']))
		session.add(row)
		# for r in data['HeavyPart']:
		# 	row = Heavypart(SrcIP=r[0],
		# 		SrcPort=r[1],
		# 		DstIP=r[2],
		# 		DstPort=r[3],
		# 		Protocol=r[4],
		# 		PktNum=r[5],
		# 		SwapFlag=r[6])
		# 	session.add(row)
		# d3 = []
		# for i in range(len(data['Distribution'])):
		# 	for l, n in data['Distribution'][i].items():
		# 		d3.append(Distribution(Client=i+1, Length=l, Num=n))
		# session.add_all(d3)
		s = 'INSERT INTO %s (SrcIP, SrcPort, DstIP, DstPort, Protocol, PktNum, SwapFlag) VALUES ' %Heavypart.__tablename__
		cmd = [s]
		cnt = 0
		for r in data['HeavyPart']:
			cnt += 1
			if cnt > 1:
				cmd.append(',')
			cmd.append('(' + str(r[0]) + ',' + str(r[1]) + ',' + str(r[2]) + ',' + str(r[3]) + ',\''
				+ str(r[4]) + '\',' + str(r[5]) + ',' + str(r[6]) + ')')
		session.execute(text(''.join(cmd)))

		for i in range(len(data['Distribution'])):
			s = 'INSERT INTO %s (Client, Length, Num) VALUES ' %Distribution.__tablename__
			cmd = [s]
			cnt = 0
			for l, n in data['Distribution'][i].items():
				cnt += 1
				if cnt > 1:
					cmd.append(',')
				cmd.append('(' + str(i + 1) + ',' + str(l) + ',' + str(n) + ')')
				if cnt > 10000:
					session.execute(text(''.join(cmd)))
					cmd = [s]
					cnt = 0
			if cnt > 0:
				session.execute(text(''.join(cmd)))
		session.commit()
		session.close()
		print('post fin!')
		print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
		return 'upload completed'
	except:
		traceback.print_exc()
		session.rollback()
		session.close()
		exc_type, exc_value, exc_traceback = sys.exc_info()
		return 'upload failed, rollback\n' + str(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))

def dbselect(session, table, field = '*', order = '', desc = False, limit = '', where = ''):
	res = []
	try:
		cmd = 'SELECT %s FROM %s' %(field, table)
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
	return res

def dbcommand(session, command):
	res = []
	try:
		t = session.execute(text(command))
		for row in t:
			res.append(list(row))
	except:
		traceback.print_exc()
	return res
