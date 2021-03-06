from GateLib import *
from MakeLogic import MakeLogic

class Parser():
	def __init__(self, filename):
		self.modulelist = list() ### if multiple modules
		self.moduleNames = dict()
		self.moduleNumber = 0 ### needed for more than one module
		self.tokenlist = list()
		self.lineEnd = True
		self.filename = filename
		self.parseFile()

	def getModuleList(self):
		return self.modulelist

	def parseFile(self):
#		try:
		fd = open(self.filename, 'r')
		line = fd.readline()
#		except:
#			print "I/O Error!"
#			return

		##### BREAKPOINT #####
		#import pdb
		#pdb.set_trace()
		######################

		while line:
			if not line.isspace():
				self.interpretLine(line)
			line = fd.readline()
		fd.close()

	def tokenize(self, line):
		##### BREAKPOINT #####
		#import pdb
		#pdb.set_trace()
		######################

		line = line.strip()
		lineEndOld = self.lineEnd

		if line.endswith(';'):
			if lineEndOld:
				tmptokenlist = self.splitLine(line)
				self.lineEnd = True
			else:
				tmptokenlist = self.splitLine(line, False)
				self.lineEnd = True
		elif line.endswith(','):
			if lineEndOld:
				tmptokenlist = self.splitLine(line)
				self.lineEnd = False
			else:
				tmptokenlist = self.splitLine(line, True)
				self.lineEnd = False
		else:
			tmptokenlist = line

		if lineEndOld:
			self.tokenlist = tmptokenlist
		else:
			i = len(self.tokenlist)
			self.tokenlist[i-1] = self.tokenlist[i-1] + tmptokenlist[0]

	def splitLine(self, line, tokenizePorts = False):
		token = str()
		tokenlist = list()
		portList = list()
		endOfLine = False

		for char in line:
			if char == ' ':
				if not tokenizePorts:
					tokenlist.append(token)
					token = ''
			elif char == '(':
				if token != '':
					tokenlist.append(token)
					token = ''
				tokenizePorts = True
			elif char == ',':
				if token != '':
					portList.append(token)
					tokenizePorts = True
					token = ''
			elif char == ';':
				if not endOfLine:
					if token != '':
						portList.append(token)
			elif char == ')':
				portList.append(token)
				tokenizePorts = False
				endOfLine = True
			else:
				token = token + char

		tokenlist.append(portList)
		return tokenlist

	def interpretLine(self, line):
		if line.startswith('//'):
			return

		self.tokenize(line)
		if not self.lineEnd:
			return

		if self.tokenlist[0] == 'module':
			self.moduleNames.update({self.tokenlist[1] : self.moduleNumber})
			self.modulelist.append(VerilogModule(self.tokenlist[1], self.tokenlist[2]))
			self.moduleNumber = self.moduleNumber + 1
		elif self.tokenlist[0] == 'reg':
			for reg in self.tokenlist[1]:
				self.modulelist[self.moduleNumber-1].addGate(REG(reg))
		elif self.tokenlist[0] == 'trireg':
			for trireg in self.tokenlist[1]:
				self.modulelist[self.moduleNumber-1].addGate(TRIREG(trireg))
		elif self.tokenlist[0] == 'input':
			self.modulelist[self.moduleNumber-1].addGate((self.tokenlist[0], self.tokenlist[1]))
		elif self.tokenlist[0] == 'output':
			self.modulelist[self.moduleNumber-1].addGate((self.tokenlist[0], self.tokenlist[1]))
		elif self.tokenlist[0] == 'wire':
			self.modulelist[self.moduleNumber-1].addGate((self.tokenlist[0], self.tokenlist[1]))
		elif self.tokenlist[0] == 'and':
			self.modulelist[self.moduleNumber-1].addGate(AND(self.tokenlist[1], self.tokenlist[2]))
		elif self.tokenlist[0] == 'or':
			self.modulelist[self.moduleNumber-1].addGate(OR(self.tokenlist[1], self.tokenlist[2]))
		elif self.tokenlist[0] == 'nand':
			self.modulelist[self.moduleNumber-1].addGate(NAND(self.tokenlist[1], self.tokenlist[2]))
		elif self.tokenlist[0] == 'nor':
			self.modulelist[self.moduleNumber-1].addGate(NOR(self.tokenlist[1], self.tokenlist[2]))
		elif self.tokenlist[0] == 'xor':
			self.modulelist[self.moduleNumber-1].addGate(XOR(self.tokenlist[1], self.tokenlist[2]))
		elif self.tokenlist[0] == 'xnor':
			self.modulelist[self.moduleNumber-1].addGate(XNOR(self.tokenlist[1], self.tokenlist[2]))
		elif self.tokenlist[0] == 'not':
			self.modulelist[self.moduleNumber-1].addGate(NOT(self.tokenlist[1], self.tokenlist[2]))
		elif self.tokenlist[0] == 'buf':
			self.modulelist[self.moduleNumber - 1].addGate(BUF(self.tokenlist[1], self.tokenlist[2]))
		elif self.tokenlist[0] == 'nmos':
			self.modulelist[self.moduleNumber-1].addGate(NMOS(self.tokenlist[1], self.tokenlist[2]))
		elif self.tokenlist[0] == 'pmos':
			self.modulelist[self.moduleNumber-1].addGate(PMOS(self.tokenlist[1], self.tokenlist[2]))
		elif self.tokenlist == 'endmodule':
			self.modulelist[self.moduleNumber-1].setEnd()
		else:
			self.modulelist[self.moduleNumber-1].addGate(ModuleAsGate(self.tokenlist[1], self.tokenlist[2]))

	def makeList(self, ports):
		tmplist = ports.rstrip(')')
		tmplist = tmplist.lstrip('(')
		tmplist = tmplist.replace(' ','')
		return tmplist.split(',')

	def checkSyntax():
			### implementation of simple syntax check possible
		return True

	def insertModules(self):
			### implementation for more than one module possible	#TODO
			self.logicDict = dict()
			mainModule = self.modulelist.pop()
			for module in self.modulelist:
				pattern = module.makePortPattern()
				tmpLogic = MakeLogic(module)
				tmpLogic.makeFunctions()
				function = tmpLogic.getFunctions()
				outp = function.get('outputs').keys()
				function = function.get(outp[0])
				self.logicDict.update({module.getName() : (pattern, function)})

			for gate in mainModule.getGateList():
				if isinstance(gate, ModuleAsGate):
					function = logicDict.get(gate.getName())
					gate.makePorts(function[0])
					gate.makeInp(function[1][1])
					gate.setFunc(function[1][0])
