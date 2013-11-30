#import tree_structure
import DynamicTree

class VerilogModule():
	def __init__(self, name, ioPorts):
		self.name = name
		self.ioPorts = PortList(ioPorts)
		self.endModule = False

	def getName(self):
		return self.name

	def getPorts(self):
		return self.ioPorts.getPorts()

	def setEnd(self):
		self.endModule = True

	def getEnd(self):
		return self.endModule

class GATE():
	def __init__(self, name, inp, outp):
		self.name = name
		self.inp = PortList('inp', inp)
		self.outp = PortList('outp' , outp)
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

class PortList():
	def __init__(self, ports):
		self.portlist = ports.rstrip(')')
		self.portlist = self.portlist.lstrip('(')
		self.portlist = self.portlist.replace(' ','')
		self.portlist = self.portlist.split(',')

	def getPorts(self):
		return self.portlist

	def equals(self, portListObj):
		tmpPortlist = portListObj.getPorts()
		for i in range(0,len(tmpPortlist)):
			if self.portlist.count(tmpPortlist[i]) == 0:
				return False

		return True

class Connections():
	def __init__(self, name):
		self.name = name
