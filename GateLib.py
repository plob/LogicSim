from copy import copy
from MakeLogic import MakeLogic

class VerilogModule():
	def __init__(self, name, ioPorts):
		self.name = name
		self.ioPorts = ioPorts
		self.endModule = False
		self.gateList = list()
		self.ConCounter = 0

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

	def setEnd(self):
		self.endModule = True

	def getEnd(self):
		return self.endModule

	def hasModule(self, name):
		for gate in self.gateList:
			if name == gate.getName():
				return True
				break
		return False

	def substitudeModule(self, name, subModule): #TODO
		for gate in self.gateList:
			if name == gate.getName():
				portsIns = gate.getInp()
				portsMod = subModule.getPorts()
				if subModule.gateList[0][0] == 'input':
					inputs = subModule.gateList[0][1]
				elif subModule.gateList[1][0] == 'input':
					inputs = subModule.gateList[1][1]
				if subModule.gateList[0][0] == 'output':
					outputs = subModule.gateList[0][1]
				elif subModule.gateList[1][0] == 'output':
					outputs = subModule.gateList[1][1]

				if (len(portsIns) - len(portsMod)):
					return 'error'


		return False

class GATE():
	def __init__(self, name, ports):
		self.name = name
		self.outp = ports[0]
		ports.remove(self.outp)
		self.inp = tuple(ports)

	def getInp(self):
		return self.inp

	def getOutp(self):
		return self.outp

	def getName(self):
		return self.name

class AND(GATE):
	def outpFunc(self, lst):
		##### BREAKPOINT #####
		#import pdb
		#pdb.set_trace()
		######################

		value = True
		for inp in len:
			value = value and inp
			if not value:
				return bool(value)
		return bool(value)

	def makeClauses(self, pinDict):
		inpNum = len(self.inp)
		outp = pinDict.get(self.outp)
		clauses = [`outp`,]
		for i in xrange(inpNum):
			inp = pinDict.get(self.inp[i])
			clauses.append('-' + `outp` + ' ' + `inp` + ' 0')
			clauses[0] = clauses[0] + ' -' + `inp`
		clauses[0] = clauses[0] + ' 0'
		return clauses

class NAND(GATE):
	def outpFunc(self, lst):
		value = True
		for inp in lst:
			value = value and inp
			if not value:
				return bool(not value)
		return bool(not value)

	def makeClauses(self, pinDict):
		inpNum = len(self.inp)
		outp = pinDict.get(self.outp)
		clauses = ['-' + `outp`,]
		for i in xrange(inpNum):
			inp = pinDict.get(self.inp[i])
			clauses.append(`outp` + ' ' + `inp` + ' 0')
			clauses[0] = clauses[0] + ' -' + `inp`
		clauses[0] = clauses[0] + ' 0'
		return clauses

class OR(GATE):
	def outpFunc(self, lst):
		value = False
		for inp in lst:
			value = value or inp
			if value:
				return bool(value)
		return bool(value)

	def makeClauses(self, pinDict):
		inpNum = len(self.inp)
		outp = pinDict.get(self.outp)
		clauses = ['-'+ `outp`,]
		for i in xrange(inpNum):
			inp = pinDict.get(self.inp[i])
			clauses.append(`outp` + ' -' + `inp` + ' 0')
			clauses[0] = clauses[0] + ' ' + `inp`
		clauses[0] = clauses[0] + ' 0'
		return clauses

class NOR(GATE):
	def outpFunc(self, lst):
		value = False
		for inp in lst:
			value = value or inp
			if value:
				return bool(not value)
		return bool(not value)

	def makeClauses(self, pinDict):
		inpNum = len(self.inp)
		outp = pinDict.get(self.outp)
		clauses = [`outp`,]
		for i in xrange(inpNum):
			inp = pinDict.get(self.inp[i])
			clauses.append('-' + `outp` + ' -' + `inp` + ' 0')
			clauses[0] = clauses[0] + ' ' + `inp`
		clauses[0] = clauses[0] + ' 0'
		return clauses

class XOR(GATE):
	def outpFunc(self, lst):
#		value = False	#function for more than 2 inputs
#		for inp in lst:
#			value = value != inp
#		return bool(value)
		return lst[0] != lst[1]

	def makeClauses(self, pinDict):
		inp0 = pinDict.get(self.inp[0])
		inp1 = pinDict.get(self.inp[1])
		outp = pinDict.get(self.outp)
		clauses = ['-' + `outp` + ' ' + `inp0` + ' ' + `inp1` + ' 0',\
					`outp` + ' -' + `inp0` + ' ' + `inp1` + ' 0',\
					`outp` + ' ' + `inp0` + ' -' + `inp1` + ' 0',\
					'-' + `outp` + ' -' + `inp0` + ' -' + `inp1` + ' 0']
		return clauses

	def makeClauses2(self, pinDict1, pinDict2):
		inp0 = pinDict1.get(self.inp[0])
		inp1 = pinDict2.get(self.inp[1])
		outp = pinDict1.get(self.outp)
		clauses = ['-' + `outp` + ' ' + `inp0` + ' ' + `inp1` + ' 0',\
					`outp` + ' -' + `inp0` + ' ' + `inp1` + ' 0',\
					`outp` + ' ' + `inp0` + ' -' + `inp1` + ' 0',\
					'-' + `outp` + ' -' + `inp0` + ' -' + `inp1` + ' 0']
		return clauses

class XNOR(GATE):
	def outpFunc(self, lst):
#		value = False
#		for inp in lst:
#			value = value == inp
#		return bool(value)
		return lst[0] == lst[1]

	def makeClauses(self, pinDict):
		inp0 = pinDict.get(self.inp[0])
		inp1 = pinDict.get(self.inp[1])
		outp = pinDict.get(self.outp)
		clauses = [`outp` + ' ' + `inp0` + ' ' + `inp1` + ' 0',\
					'-' + `outp` + ' -' + `inp0` + ' ' + `inp1` + ' 0',\
					'-' + `outp` + ' ' + `inp0` + ' -' + `inp1` + ' 0',\
					`outp` + ' -' + `inp0` + ' -' + `inp1` + ' 0']
		return clauses

class NOT(GATE):
	def outpFunc(self, lst):
		return (not lst[0])

	def makeClauses(self, pinDict):
		inp = pinDict.get(self.inp[0])
		outp = pinDict.get(self.outp)
		clauses = [`outp` + ' ' + `inp` + ' 0',\
					'-' + `outp` + ' -' + `inp` + ' 0']
		return clauses

class BUF(GATE):
	def outpFunc(self, lst):
		return (lst[0])

	def makeClauses(self, pinDict):
		inp = pinDict.get(self.inp[0])
		outp = pinDict.get(self.outp)
		clauses = ['-' + `outp` + ' ' + `inp` + ' 0',\
					`outp` + ' -' + `inp` + ' 0']
		return clauses

class MOS(GATE):
	def __init__(self, name, ports):
		GATE.__init__(self, name, ports)
		self.gate = self.inp[1]
		self.inp = self.inp[0]

class NMOS(MOS):
	def outpFunc(self, lst):
		if lst[1]:
			return lst[0]
		else:
			return 'Z'

	def makeClauses(self, pinDict):
		inp = pinDict.get(self.inp[0])
		outp = pinDict.get(self.outp)
		#TODO
		return clauses

class PMOS(MOS):
	def outpFunc(self, lst):
		if not lst[1]:
			return lst[0]
		else:
			return 'Z'

	def makeClauses(self, pinDict):
		inp = pinDict.get(self.inp[0])
		outp = pinDict.get(self.outp)
		#TODO
		return clauses

class REG(GATE):
	def __init__(self, name):
		GATE.__init__(self, name, ['out', 'in'])
		self.lastValue = False

	def outpFunc(self, lst):
		outp = self.lastValue
		self.lastValue = lst[0]
		return outp

	def makeClauses(self, pinDict):
		inp = pinDict.get(self.inp[0])
		outp = pinDict.get(self.outp)
		#TODO
		return clauses

class TRIREG(GATE):
	def __init__(self, name):
		GATE.__init__(self, name, ['out', 'in'])
		self.lastValue = False

	def outpFunc(self, lst):
		if lst[0] == 'Z':
			return self.lastValue
		else:
			outp = self.lastValue
			self.lastValue = lst[0]
		return lst[0]

	def makeClauses(self, pinDict):
		inp = pinDict.get(self.inp[0])
		outp = pinDict.get(self.outp)
		#TODO
		return clauses
