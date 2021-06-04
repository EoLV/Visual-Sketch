import math
from functools import reduce
import threading
import time

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from . import models
from .sessions import dbinsert, dbinsert_all, dbselect, dbdelete, dbcommand

# 初始化数据表模板类
Base = declarative_base()
M_Sys_Info = models.getmodel_sys_info(Base)
M_Data_Info = models.getmodel_data_info(Base)
M_Distribution = models.getmodel_distribution(Base)
M_Client_Statistics = models.getmodel_client_statistics(Base)
M_Elephant_Flows = models.getmodel_elephant_flows(Base)
M_Clients = models.getmodel_clients(Base)
M_Flows = models.getmodel_flows(Base)

class ReadCache:
	def __init__(self):
		self.elephant_flows = {}
		self.distribution = {}
		self.client_statistics = {}
		self.client_addr = {}
		self.clients = {}



class SaveCache:
	def __init__(self):
		self.client_count = 0
		self.cid_cache = {}
		self.unsaved_client = []

		self.flow_count = 0
		self.fid_cache = {}
		self.unsaved_flow = []

		self.fsize_cache = {}

	def update(self, session):
		maxcid = dbselect(session, M_Clients, 'max(cid)')[0][0]
		maxcid = maxcid if maxcid else 0
		self.client_count = max(self.client_count, maxcid)
		maxfid = dbselect(session, M_Flows, 'max(fid)')[0][0]
		maxfid = maxfid if maxfid else 0
		self.flow_count = max(self.flow_count, maxfid)

	def flush(self, session):
		dbinsert_all(session, M_Clients, self.unsaved_client)
		self.unsaved_client = []
		dbinsert_all(session, M_Flows, self.unsaved_flow)
		self.unsaved_flow = []

	def get_cid(self, session, address):
		if address not in self.cid_cache:
			result = dbselect(session, M_Clients, field='cid', where='addr=%d' %address)
			if len(result) > 0:
				self.cid_cache[address] = result[0][0]
			else:
				self.client_count += 1
				self.cid_cache[address] = self.client_count
				self.unsaved_client.append([self.client_count, address])
		return self.cid_cache[address]

	def get_fid(self, fivetuple):
		if fivetuple not in self.fid_cache:
			self.flow_count += 1
			self.fid_cache[fivetuple] = self.flow_count
			self.unsaved_flow.append([self.flow_count, fivetuple[0], fivetuple[1],
				fivetuple[2], fivetuple[3], fivetuple[4]])
		return self.fid_cache[fivetuple]

	def get_increment(self, fid, size):
		if fid not in self.fsize_cache:
			self.fsize_cache[fid] = size
		result = size - self.fsize_cache[fid]
		self.fsize_cache[fid] = size
		return result

class DBData:
	def __init__(self, url):
		# 初始化数据库连接
		self.DBEngine = sqlalchemy.create_engine(url)#, echo=True)
		self.DBSession = scoped_session(sessionmaker(bind=self.DBEngine))

		# 建立数据表
		Base.metadata.create_all(bind=self.DBEngine)

		self.system_status = 0
		self.status_timer = None

		self.svcache = SaveCache()
		self.rdcache = ReadCache()

	def clean(self):
		Base.metadata.drop_all(bind=self.DBEngine)
		Base.metadata.create_all(bind=self.DBEngine)

		self.system_status = 0
		self.status_timer = None

		self.svcache = SaveCache()
		self.rdcache = ReadCache()

	def set_sys_info(self, status, addr = 0, port = 0, agent = ''):
		session = self.DBSession()
		if status == 1:
			# 定时器，10秒没有新数据进入时标记状态为0
			if self.status_timer:
				self.status_timer.cancel()
			self.status_timer = threading.Timer(10, self.set_sys_info, [0])
			self.status_timer.start()

			if self.system_status == 0:
				dbdelete(session, M_Sys_Info)
				nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
				dbinsert(session, M_Sys_Info, [1, nowtime, addr, port, agent])
		if status == 0:
			if self.system_status == 1:
				dbcommand(session, 'UPDATE sys_info SET status = 0')
		self.system_status = status
		session.close()

	def save_data(self, rawdata):
		# 源数据中Clients数量和编号给定，192.168.1.2编号为1，依此类推
		# 这大概也是那边偷的懒
		# 反正就先写死在这里了
		session = self.DBSession()
		dbinsert_all(session, M_Clients, [[1, 3232235778], [2, 3232235779], [3, 3232235780],
			[4, 3232235781], [5, 3232235782], [6, 3232235783], [7, 3232235784], [8, 3232235785]])
		session.close()

		tid = rawdata['ID']
		time = rawdata['Time']
		data_type = rawdata['Algorithm']
		entropy = rawdata['Entropy']
		flow_count = 0
		traffic_count = 0

		new_clients = []
		new_flows = []

		distribution = []
		client_statistics = []
		element_flows = []

		cid = 0
		for client in rawdata['Distribution']:
			cid += 1
			c_flow_count = 0
			c_traffic_count = 0
			for item in client:
				distribution.append([tid, cid, item[0], item[1]])
				c_flow_count += item[1]
				c_traffic_count += item[0] * item[1]
			client_statistics.append([tid, cid, c_flow_count, c_traffic_count, 0])
			flow_count += c_flow_count
			traffic_count += c_traffic_count

		session = self.DBSession()

		self.svcache.update(session)

		for item in rawdata['HeavyPart']:
			# 源数据格式：[srcIP, dstIP, srcPort, dstPort, protocol, flowsize]
			# 源数据中srcIP, dstIP大端序小端序是反的（大概是那边的bug）
			convert_endian = lambda x: reduce(lambda a, b: a + b, [x//(256**i)%256*(256**(3-i)) for i in range(3,-1,-1)][::-1])
			src = self.svcache.get_cid(session, convert_endian(item[0]))
			dst = self.svcache.get_cid(session, convert_endian(item[1]))
			fivetuple = (src, dst, item[2], item[3], item[4])
			fid = self.svcache.get_fid(fivetuple)
			increment = self.svcache.get_increment(fid, item[5])
			element_flows.append([tid, fid, item[5], increment])

		self.svcache.flush(session)
		dbinsert(session, M_Data_Info, [tid, time, data_type, flow_count, traffic_count, entropy, 0])
		dbinsert_all(session, M_Distribution, distribution)
		dbinsert_all(session, M_Client_Statistics, client_statistics)
		dbinsert_all(session, M_Elephant_Flows, element_flows)
		session.close()

		self.delete_old(tid)

	def delete_old(self, tid):
		oldtid = tid - 4 * ((tid - 1) & -(tid - 1))

		if oldtid > 1:
			session = self.DBSession()
			dbcommand(session, 'UPDATE data_info SET deleted = 1 WHERE tid=%d' %oldtid)
			dbdelete(session, M_Distribution, where='tid=%d' %oldtid)
			dbdelete(session, M_Client_Statistics, where='tid=%d' %oldtid)
			dbdelete(session, M_Elephant_Flows, where='tid=%d' %oldtid)
			session.close()

	def get_sys_info(self):
		session = self.DBSession()
		data = dbselect(session, M_Sys_Info, field='status, start_time, source_addr, source_port, source_agent')
		session.close()
		result = data[0]
		return result

	# 返回字典格式：{tid: [tid, time, flow_count, traffic_count, entropy]}
	def get_data_info(self):
		session = self.DBSession()
		data = dbselect(session, M_Data_Info, field='tid, time, flow_count, traffic_count, entropy', where='deleted=0')
		session.close()
		result = { item[0] : item for item in data }
		return result

	# 返回列表格式：[[fid, src, dst, src_port, dst_port, protocol, size, increment]]
	def get_elephant_flows(self, tid):
		if tid not in self.rdcache.elephant_flows:
			session = self.DBSession()
			result = dbcommand(session, 'SELECT flows.fid, flows.src, flows.dst, flows.src_port, flows.dst_port, flows.protocol, 	elephant_flows.size, elephant_flows.increment FROM elephant_flows INNER JOIN flows ON elephant_flows.fid=flows.	fid WHERE tid=%d' %tid)
			session.close()
			self.rdcache.elephant_flows[tid] = result
		return self.rdcache.elephant_flows[tid]

	# [[cid, size, count]]
	def get_distribution(self, tid):
		if tid not in self.rdcache.distribution:
			session = self.DBSession()
			result = dbselect(session, M_Distribution, field='cid, size, count', where='tid=%d' %tid)
			session.close()
			self.rdcache.distribution[tid] = result
		return self.rdcache.distribution[tid]

	# [[cid, flow_count, traffic_count, entropy]]
	def get_client_statistics(self, tid):
		if tid not in self.rdcache.client_statistics:
			session = self.DBSession()
			result = dbselect(session, M_Client_Statistics, field='cid, flow_count, traffic_count, entropy', where='tid=%d' %tid)
			session.close()
			self.rdcache.client_statistics[tid] = result
		return self.rdcache.client_statistics[tid]

	# [[tid, time, size]]
	def get_flow_history(self, fid):
		session = self.DBSession()
		data = dbcommand(session, 'SELECT data_info.tid, data_info.time, elephant_flows.size FROM elephant_flows INNER JOIN data_info ON data_info.tid=elephant_flows.tid WHERE fid=%d' %fid)
		session.close()
		return data

	def get_client_addr(self, cid):
		if cid not in self.rdcache.client_addr:
			session = self.DBSession()
			data = dbselect(session, M_Clients, field='addr', where='cid=%d' %cid)
			session.close()
			self.rdcache.client_addr[cid] = data[0][0]
		return self.rdcache.client_addr[cid]

	def get_clients(self, tid):
		if tid not in self.rdcache.clients:
			session = self.DBSession()
			result = dbcommand(session, 'SELECT clients.cid, clients.addr, client_statistics.flow_count, client_statistics.traffic_count FROM clients INNER JOIN client_statistics on clients.cid = client_statistics.cid WHERE client_statistics.tid = %d' %tid)
			session.close()
			self.rdcache.clients[tid] = result
		return self.rdcache.clients[tid]

	def reflesh(self):
		self.rdcache = ReadCache()
