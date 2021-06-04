import math
from functools import reduce
import numpy as np

from ..dbconsole import dbdata

class PGData:
	def __init__(self, url):
		self.db = dbdata.DBData(url)

	def get_pgsysinfo_data(self, tid):
		sys_info = self.db.get_sys_info()
		clients = self.db.get_clients(tid)
		time = self.get_data_info()[tid][1]
		return { 'sys_info': sys_info, 'clients': clients, 'time': time }

	def get_pgtraffic_data(self, tid):
		data_attr = self.get_data_info()[tid]
		elephant_flows = self.get_elephant_flows(tid)
		client_statistics = self.db.get_client_statistics(tid)
		return { 'data_attr': data_attr, 'elephant_flows': elephant_flows, 'client_statistics': client_statistics }

	def get_pgdistri_data(self, tid):
		data_attr = self.get_data_info()[tid]
		distribution = self.db.get_distribution(tid)
		client_statistics = self.db.get_client_statistics(tid)
		maxsize = max(distribution, key=lambda x: x[1])[1]
		return { 'data_attr': data_attr, 'distribution': distribution, 'client_statistics': client_statistics, 'maxsize': maxsize }

	def get_pgelephant_data(self, tid):
		return self.get_elephant_flows(tid)

	def get_pgflows_data(self, tid):
		return self.get_elephant_flows(tid)

	def get_elephant_flows(self, tid):
		return self.db.get_elephant_flows(tid)

	def get_client_addr(self, cid):
		return self.db.get_client_addr(cid)

	def get_data_info(self):
		return self.db.get_data_info()

	def get_tid(self, dataid):
		data_info = self.get_data_info()
		if dataid and int(dataid) in data_info.keys():
			return int(dataid)
		return sorted(data_info.keys())[-1]

	def get_flow_history(self, fid):
		return self.db.get_flow_history(fid)

	def reflesh(self):
		return self.db.reflesh()
