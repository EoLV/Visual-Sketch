from . import sessions
import numpy as np
from functools import reduce
import math

class data:
	def __init__(self, _DBSession):
		self.DBSession = _DBSession
		self.d_attrid = []
		self.d_allflow = {}
		self.d_traffic = {}
		self.d_distribution = {}

	def reflesh(self):
		self.d_attrid = []
		self.d_allflow = {}
		self.d_traffic = {}
		self.d_distribution = {}

	def attrid(self, reflesh=False):
		if reflesh or not self.d_attrid:
			session = self.DBSession()
			data = sessions.dbselect(session, 'attribute', \
				field='ID,Time,Cardinality,Entropy', order='ID')
			self.d_attrid = { t[0] : t for t in data }
			session.close()
		if self.d_attrid:
			return self.d_attrid
		return { 0: [0, '0', 0, 0] }

	def allflow(self, idt):
		if idt in self.d_allflow:
			return self.d_allflow[idt]
		session = self.DBSession()
		res = sessions.dbselect(session, \
			str(idt)+'_heavypart', \
			field='SrcIP,SrcPort,DstIP,DstPort,Protocol,PktNum,SwapFlag,ID')
		session.close()
		if res:
			self.d_allflow[idt] = res
		return res

	def distribution(self, idt):
		if idt in self.d_distribution:
			return self.d_distribution[idt]

		flow100 = [[0 for i in range(1001)] for i in range(8)]
		pkt100 = [[0 for i in range(1001)] for i in range(8)]
		flowpie = [[0 for i in range(6)] for i in range(8)]
		pktpie = [[0 for i in range(6)] for i in range(8)]
		flowall = [0 for i in range(8)]
		pktall = [0 for i in range(8)]
		entropy = [0 for i in range(8)]
		flowant = [[0 for i in range(501)] for i in range(8)]
		pktant = [[0 for i in range(501)] for i in range(8)]
		# xaxisdata = [i * 10 for i in range(0, f[9] + 1)]
		xaxisdata = [i for i in range(1001)]
		maxlen = 1
		base = 1

		divpoint = [20, 50, 200, 500, 2000, 1e10]

		session = self.DBSession()
		res = sessions.dbselect(session, \
			str(idt)+'_distribution', field='Client,Length,Num')
		session.close()
		if res:
			for i in res:
				maxlen = max(maxlen, i[1])
			while base * 1000 < maxlen:
				base *= 10
			for i in res:
				c = i[0] - 1
				l = i[1]
				n = i[2]
				flow100[c][min((l-1)//base + 1, 1000)] += n
				pkt100[c][min((l-1)//base + 1, 1000)] += l * n
				serie = 0
				for i in range(6):
					if l < divpoint[i]:
						serie = i
						break
				flowpie[c][serie] += n
				pktpie[c][serie] += l * n
				flowall[c] += n
				pktall[c] += l * n
				if l <= 500:
					flowant[c][l] += n
					pktant[c][l] += l * n
			for i in res:
				c = i[0] - 1
				l = i[1]
				n = i[2]
				m = flowall[c]
				entropy[c] -= l * n / m * math.log(n / m)
			maxlen = min((maxlen-1)//base + 1, 1000)
			xaxisdata = [i * base for i in range(maxlen + 1)]
			self.d_distribution[idt] = [flow100, pkt100, flowpie, pktpie, flowall, pktall, entropy, flowant, pktant, maxlen, xaxisdata]
		return [flow100, pkt100, flowpie, pktpie, flowall, pktall, entropy, flowant, pktant, maxlen, xaxisdata]

	def traffic(self, idt):
		if idt in self.d_traffic:
			return self.d_traffic[idt]
		allflow = self.allflow(idt)
		elephanttraffic = np.zeros((8, 8), dtype=np.int64)
		elephantflow = np.zeros((8, 8), dtype=np.int)
		for i in allflow:
			try:
				elephanttraffic[self.iptocid(i[2])][self.iptocid(i[0])] += i[5]
				elephantflow[self.iptocid(i[2])][self.iptocid(i[0])] += 1
			except:
				pass
		pktall = self.distribution(idt)[5]
		flowall = self.distribution(idt)[4]
		traffic = reduce(lambda x, y: x + y, pktall)
		flow = reduce(lambda x, y: x + y, flowall)
		self.d_traffic[idt] = [elephanttraffic, elephantflow, pktall, flowall, traffic, flow]
		return [elephanttraffic, elephantflow, pktall, flowall, traffic, flow]

	def cidtoip(self, cid):
		if cid == 0:
			return 3232235778
		if cid == 1:
			return 3232235779
		if cid == 2:
			return 3232235780
		if cid == 3:
			return 3232235781
		if cid == 4:
			return 3232235782
		if cid == 5:
			return 3232235783
		if cid == 6:
			return 3232235784
		if cid == 7:
			return 3232235785
		return -1

	def iptocid(self, cid):
		if cid == 3232235778:
			return 0
		if cid == 3232235779:
			return 1
		if cid == 3232235780:
			return 2
		if cid == 3232235781:
			return 3
		if cid == 3232235782:
			return 4
		if cid == 3232235783:
			return 5
		if cid == 3232235784:
			return 6
		if cid == 3232235785:
			return 7
		return -1
