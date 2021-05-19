import sqlalchemy
from sqlalchemy import Column, create_engine, String, Float, DECIMAL, Boolean, Enum, Date, DateTime, Time
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.ext.declarative import declarative_base

def make_attribute(base):
	class Attribute(base):
		__tablename__ = 'attribute'
		__table_args__ = {"extend_existing": True}
		ID = Column(INTEGER(unsigned=True), primary_key=True)
		Algorithm = Column(Enum('elastic'))
		Time = Column(String(30))
		Cardinality = Column(INTEGER(unsigned=True))
		Entropy = Column(String(20))
		def __repr__(self):
			return "Data {}".format(self.ID)
	return Attribute

def make_heavypart(base, id):
	class Heavypart(base):
		__tablename__ = str(id) + '_heavypart'
		__table_args__ = {"extend_existing": True}
		ID = Column(INTEGER(unsigned=True), primary_key=True)
		SrcIP = Column(INTEGER(unsigned=True))
		SrcPort = Column(SMALLINT(unsigned=True))
		DstIP = Column(INTEGER(unsigned=True))
		DstPort = Column(SMALLINT(unsigned=True))
		Protocol = Column(String(10))
		PktNum = Column(INTEGER(unsigned=True))
		SwapFlag = Column(Boolean)
	return Heavypart

def make_lightpart(base, id):
	class Lightpart(base):
		__tablename__ = str(id) + '_lightpart'
		__table_args__ = {"extend_existing": True}
		ID = Column(INTEGER(unsigned=True), primary_key=True)
		Hash = Column(INTEGER(unsigned=True))
		PktNum = Column(INTEGER(unsigned=True))
	return Lightpart

def make_distribution(base, id):
	class Distribution(base):
		__tablename__ = str(id) + '_distribution'
		__table_args__ = {"extend_existing": True}
		ID = Column(INTEGER(unsigned=True), primary_key=True)
		Client = Column(INTEGER(unsigned=True))
		Length = Column(INTEGER(unsigned=True))
		Num = Column(INTEGER(unsigned=True))
	return Distribution
