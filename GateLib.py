from copy import copy
#from DynamicTree import DynamicTree

class VerilogModule():
	def __init__(self, name, ioPorts):
		self.name = name
		self.ioPorts = ioPorts
		self.endModule = False
		self.gateList = list()

	def addGate(self, obj):
		self.gateList.append(obj)

	def getNode(self):
		return self.node

	def getGateList(self):
		return self.gateList

	def getName(self):
		return self.name

	def getPorts(self):
		return self.ioPorts

#	def appendPorts(self, ports):
#		self.ioPorts.append(ports)

	def setEnd(self):
		self.endModule = True

	def getEnd(self):
		return self.endModule


class PortList():
	def __init__(self, ports):
		self.portlist = self.makeList(ports)

	def makeList(self, ports):
		tmplist = ports.rstrip(')')
		tmplist = tmplist.lstrip('(')
		tmplist = tmplist.replace(' ','')
		return tmplist.split(',')

	def makeInp(self):
		self.portlist.reverse()
		self.portlist.pop()
		self.portlist.reverse()

	def makeOutp(self):
		self.portlist = self.portlist[0]

	def getPorts(self):
		return self.portlist

	def append(self, ports):
		tmpList = self.makeList(ports)
		self.portlist.append(tmplist)

	def equals(self, portListObj):
		tmpPortlist = portListObj.getPorts()
		for i in xrange(len(tmpPortlist)):
			if self.portlist.count(tmpPortlist[i]) == 0:
				return False

		return True

#class Connections():
#	def __init__(self, name):
#		self.name = name

class GATE():
	def __init__(self, name, ports):
		self.name = name
		self.outp = ports[0]
		ports.remove(self.outp)
		self.inp = ports

	def getInp(self):
		return copy(self.inp)

	def getOutp(self):
		return copy(self.outp)

	def getName(self):
		return copy(self.name)

class AND(GATE):
	def outpFunc(self, lst):
		##### BREAKPOINT #####
		#import pdb
		#pdb.set_trace()
		######################

		value = True
		for i in xrange(len(self.inp)):
			nextInp = lst.pop()
			value = value and nextInp
#			if not value:
#				return lst + [value]
		return lst + [bool(value)]

class NAND(GATE):
	def outpFunc(self, lst):
		value = True
		for i in xrange(len(self.inp)):
			nextInp = lst.pop()
			value = value and nextInp
#			if not value:
#				return lst + [not value]
		return lst + [bool(not value)]

class OR(GATE):
	def outpFunc(self, lst):
		value = False
		for i in xrange(len(self.inp)):
			nextInp = lst.pop()
			value = value or nextInp
#			if value:
#				return lst + [value]
		return lst + [bool(value)]

class NOR(GATE):
	def outpFunc(self, lst):
		value = False
		for i in xrange(len(self.inp)):
			nextInp = lst.pop()
			value = value or nextInp
#			if value:
#				return lst + [not value]
		return lst + [bool(not value)]

class XOR(GATE):
	def outpFunc(self, lst):
		value = False
		for i in xrange(len(self.inp)):
			nextInp = lst.pop()
			value = value != nextInp
		return lst + [bool(value)]

class NOT(GATE):
	def outpFunc(self, lst):
		lst.append(not lst.pop())
		return lst

