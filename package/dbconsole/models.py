import sqlalchemy
from sqlalchemy import Column, create_engine, String, Float, DECIMAL, Boolean, Enum, Date, DateTime, Time, BigInteger
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.ext.declarative import declarative_base

def getmodel_sys_info(base):
	class Sys_Info(base):
		__tablename__ = 'sys_info'
		__table_args__ = {"extend_existing": True}
		status = Column(INTEGER)
		start_time = Column(String(30), primary_key=True)
		source_addr = Column(String(16))
		source_port = Column(INTEGER(unsigned=True))
		source_agent = Column(String(50))
	return Sys_Info

def getmodel_data_info(base):
	class Data_Info(base):
		__tablename__ = 'data_info'
		__table_args__ = {"extend_existing": True}
		tid = Column(INTEGER(unsigned=True), primary_key=True)
		time = Column(String(30))
		data_type = Column(String(20))
		flow_count = Column(BigInteger)
		traffic_count = Column(BigInteger)
		entropy = Column(Float)
		deleted = Column(Boolean)
	return Data_Info

def getmodel_distribution(base):
	class Distribution(base):
		__tablename__ = 'distribution'
		__table_args__ = {"extend_existing": True}
		tid = Column(INTEGER(unsigned=True), primary_key=True)
		cid = Column(INTEGER(unsigned=True), primary_key=True)
		size = Column(BigInteger, primary_key=True)
		count = Column(BigInteger)
	return Distribution

def getmodel_client_statistics(base):
	class Client_Statistics(base):
		__tablename__ = 'client_statistics'
		__table_args__ = {"extend_existing": True}
		tid = Column(INTEGER(unsigned=True), primary_key=True)
		cid = Column(INTEGER(unsigned=True), primary_key=True)
		flow_count = Column(BigInteger)
		traffic_count = Column(BigInteger)
		entropy = Column(Float)
	return Client_Statistics

def getmodel_elephant_flows(base):
	class Elephant_Flows(base):
		__tablename__ = 'elephant_flows'
		__table_args__ = {"extend_existing": True}
		tid = Column(INTEGER(unsigned=True), primary_key=True)
		fid = Column(INTEGER(unsigned=True), primary_key=True)
		size = Column(BigInteger)
		increment = Column(BigInteger)
	return Elephant_Flows

def getmodel_clients(base):
	class Clients(base):
		__tablename__ = 'clients'
		__table_args__ = {"extend_existing": True}
		cid = Column(INTEGER(unsigned=True), primary_key=True, autoincrement = True)
		addr = Column(INTEGER(unsigned=True))
	return Clients

def getmodel_flows(base):
	class Flows(base):
		__tablename__ = 'flows'
		__table_args__ = {"extend_existing": True}
		fid = Column(INTEGER(unsigned=True), primary_key=True, autoincrement = True)
		src = Column(INTEGER(unsigned=True))
		dst = Column(INTEGER(unsigned=True))
		src_port = Column(INTEGER(unsigned=True))
		dst_port = Column(INTEGER(unsigned=True))
		protocol = Column(String(20))
	return Flows
