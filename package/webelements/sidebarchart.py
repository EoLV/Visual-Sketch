import numpy as np
from functools import reduce

def attrchart(data, attrid):
	attr = data.attrid()
	f = data.allflow(attr[0])
