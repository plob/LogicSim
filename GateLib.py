from copy import copy
#from MakeLogic import MakeLogic

class VerilogModule():
	def __init__(self, name, ioPorts):
		self.name = name
		self.ioPorts = ioPorts
		self.endModule = False
		self.gateList = list()
		self.ConCounter = 0
		self.ioMap = dict()

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

#	def makeIOmap(self):
#		i = 0
#		for port in self.ioPorts:
#			if self.gateList[0][1].count(port):
#				self.ioMap.update({i : self.gateList[0][1].index(port)

	def hasModule(self, name):
		for gate in self.gateList:
			if name == gate.getName():
				return True
				break
		return False

	def makePortPattern(self):
		i = 0
		portPattern = dict()
		inputs = self.gateList[0][1]
		outputs = self.gateList[1][1]
		for inp in inputs:
			portPattern.update({'in_'+`i` : (self.ioPorts.index(inp), inp)})
			i = i + 1
		for outp in outputs:
			portPattern.update({'out' : self.ioPorts.index(outp)})

		return portPattern

class GATE():
	def __init__(self, name, ports):
		self.name = name
		self.outp = ports[0]
		ports.remove(self.outp)
		self.inp = ports

	def getInp(self):
		return self.inp

	def getOutp(self):
		return self.outp

	def getName(self):
		return self.name

class ModuleAsGate(GATE):
	def __init__(self, name, ports):
		GATE.__init__(self, name, ['dummy_out',] + ports)

	def setFunc(self, func):
		self.function = func

	def makePorts(self, pattern):
		self.outp = self.inp[pattern.get('out')]
		tmpInp = list()
		self.inpDict = dict()
		for i in xrange(len(self.inp)-1):
			tmp = pattern.get('in_'+`i`)
			tmpInp.append(self.inp[tmp[0]])
			self.inpDict.update({tmp[1] : self.inp[pattern.get(tmp[0])]})
		self.inp = tmpInp

	def makeInp(self, pattern):
		newInpts = list()

		for element in pattern:
			if isinstance(element, list):
				newInpts.append(self.makeInp(element))
			else:
				newInpts.append(self.inpDict.get(element))
		self.inp = newInpts
		return newInpts

	def outpFunc(self, lst):
		return self.function(lst)

	def makeClauses(self, pinDict):
		#TODO
		return clauses

class AND(GATE):
	def outpFunc(self, lst):
		##### BREAKPOINT #####
		#import pdb
		#pdb.set_trace()
		######################

		value = True
		for inp in lst:
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

	def getInp(self):
		return [self.inp, self.gate]

class NMOS(MOS):
	def outpFunc(self, lst):
		if lst[1]:
			print 'nmos ' + `self.name` + ' ' + `lst[0]`
			return lst[0]
		else:
			print 'nmos ' + `self.name` + ' ' + 'Z'
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
		GATE.__init__(self, name, [name+'_out', name])
		self.lastValue = 'Z'

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
		GATE.__init__(self, name, [name+'_out', name])
		self.lastValue = 'Z'

	def outpFunc(self, lst):
		if lst[0] == 'Z':
			print 'trireg ' + `self.name` + ' ' + `self.lastValue`
			return self.lastValue
		else:
			outp = self.lastValue
			self.lastValue = lst[0]
		print 'trireg ' + `self.name` + ' ' + `lst[0]`
		return lst[0]

	def makeClauses(self, pinDict):
		inp = pinDict.get(self.inp[0])
		outp = pinDict.get(self.outp)
		#TODO
		return clauses
