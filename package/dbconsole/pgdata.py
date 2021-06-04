import math
from functools import reduce
import threading
import time

import numpy as np

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from .sessions import dbselect, dbcommand

class PGData:
	def __init__(self, url):
		# 初始化数据库连接
		self.DBEngine = sqlalchemy.create_engine(url)#, echo=True)
		self.DBSession = scoped_session(sessionmaker(bind=self.DBEngine))

	def get_sys_info(self):
		session = self.DBSession()
		data = dbselect(session, 'sys_info', field='status, start_time, source_addr, source_port, source_agent')
		session.close()
		result = data[0]
		return result

	# 返回字典格式：{tid: [tid, time, flow_count, traffic_count, entropy]}
	def get_data_info(self):
		session = self.DBSession()
		data = dbselect(session, 'data_info', field='tid, time, flow_count, traffic_count, entropy', where='deleted=0')
		session.close()
		result = { item[0] : item for item in data }
		return result

	# 返回列表格式：[[fid, src, dst, src_port, dst_port, protocol, size, increment]]
	def get_elephant_flows(self, tid):
		session = self.DBSession()
		data = dbcommand(session, 'SELECT flows.fid, flows.src, flows.dst, flows.src_port, flows.dst_port, flows.protocol, elephant_flows.size, elephant_flows.increment FROM elephant_flows INNER JOIN flows ON elephant_flows.fid=flows.fid WHERE tid=%d' %tid)
		session.close()
		return data

	def get_distribution(self, tid):
		session = self.DBSession()
		data = dbselect(session, 'distribution', field='cid, size, count', where='tid=%d' %tid)
		session.close()
		return data

	def get_client_statistics(self, tid):
		session = self.DBSession()
		data = dbselect(session, 'client_statistics', field='cid, flow_count, traffic_count, entropy', where='tid=%d' %tid)
		session.close()
		return data

	def get_flow_history(self, fid):
		session = self.DBSession()
		data = dbcommand('SELECT data_info.tid, data_info.time, elephant_flows.size FROM elephant_flows INNER JOIN data_info ON data_info.tid=elephant_flows.tid WHERE fid=%d' %fid)
		session.close()
		return data

	def get_client_addr(self, cid):
		session = self.DBSession()
		data = dbselect(session, 'clients', field='addr', where='cid=%d' %cid)
		session.close()
		return data[0][0]

