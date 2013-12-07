#from copy import copy
#from DynamicTree import DynamicTree

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

	def substitudeModule(self, name, subGateList): #TODO
		for gate in self.gateList:
			if name == gate.getName():
				#ports equal? additional check possible
				inputs = dict()
				outputs = dict()
				wires = dict()
				#for item in subGateList:
				#	if isinstance(item, tuple):
				#		if item[0] == 'input':
				#			inputs.update({item[1] : self.ConCounter})
				#			subGateList.remove(item)
				#		elif item[0] == 'output':
				#			outputs = item[1]
				#			subGateList.remove(item)
				#		elif item[0] == 'wire':
				#			wires = item[1]
				#			subGateList.remove(item)
				#		else:
				#			None
				#	else:
				#		break
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
		for i in xrange(len(self.inp)):
			nextInp = lst.pop()
			value = value and nextInp
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
		for i in xrange(len(self.inp)):
			nextInp = lst.pop()
			value = value and nextInp
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
		for i in xrange(len(self.inp)):
			nextInp = lst.pop()
			value = value or nextInp
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
		for i in xrange(len(self.inp)):
			nextInp = lst.pop()
			value = value or nextInp
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
		value = False
		for i in xrange(len(self.inp)):
			nextInp = lst.pop()
			value = value != nextInp
		return bool(value)

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

class NOT(GATE):
	def outpFunc(self, lst):
		return (not lst.pop())

	def makeClauses(self, pinDict):
		inp = pinDict.get(self.inp[0])
		outp = pinDict.get(self.outp)
		clauses = [`outp` + ' ' + `inp` + ' 0',\
					'-' + `outp` + ' -' + `inp` + ' 0']
		return clauses

