#import tree_structure
from DynamicTree import DynamicTree

class VerilogModule():
	def __init__(self, name, ioPorts):
		self.name = name
		self.ioPorts = PortList(ioPorts)
		self.endModule = False

	def getName(self):
		return self.name

	def getPorts(self):
		return self.ioPorts.getPorts()

	def appendPorts(self, ports):
		self.ioPorts.append(ports)

	def setEnd(self):
		self.endModule = True

	def getEnd(self):
		return self.endModule


class PortList():
	def __init__(self, ports):
		self.portlist = self.makeList(ports)

	def makeList(self, ports):
		tmplist = ports.rstrip(')')
		tmplist = self.portlist.lstrip('(')
		tmplist = self.portlist.replace(' ','')
		return self.portlist.split(',')

	def getPorts(self):
		return self.portlist

	def append(self, ports):
		tmpList = self.makeList(ports)
		self.portlist.append(tmplist)

	def equals(self, portListObj):
		tmpPortlist = portListObj.getPorts()
		for i in range(0,len(tmpPortlist)):
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
		self.outp = PortList(ports)
		return

	def getName(self):
		return self.name

class AND(GATE):
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

