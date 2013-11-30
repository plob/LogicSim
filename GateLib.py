#import tree_structure
#from DynamicTree import DynamicTree

class VerilogModule():
	def __init__(self, name, ioPorts):
		self.name = name
		self.ioPorts = PortList(ioPorts)
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
		return self.ioPorts.getPorts()

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

		self.inp = PortList(ports)
		self.inp.makeInp()

		self.outp = PortList(ports)
		self.inp.makeOutp()
		self.outp = self.outp.getPorts()
		self.outp = self.outp[0]

	def getInp(self):
		return self.inp

	def getName(self):
		return self.name

class AND(GATE):
	def outpFunc(self):
		inpList = self.inp.getPorts()
		func = dict()

		for i in xrange(len(inpList)):
			func = func.update({self.outp : gateFunc(func.get(self.outp), inpList[i])})



	def evaluate(self, inp):	#TODO: write evaluate function for all gates
		return

class NAND(GATE):
	def evaluate(self, inp):	#TODO: write evaluate function for all gates
		return

class OR(GATE):
	def evaluate(self, inp):	#TODO: write evaluate function for all gates
		return

class NOR(GATE):
	def evaluate(self, inp):	#TODO: write evaluate function for all gates
		return

class XOR(GATE):
	def evaluate(self, inp):	#TODO: write evaluate function for all gates
		return

class NOT(GATE):
	def evaluate(self, inp):	#TODO: write evaluate function for all gates
		return

