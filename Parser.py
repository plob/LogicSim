from GateLib import *

class Parser():
	def __init__(self, filename):
		self.modulelist = list()
		self.moduleNumber = 0
		self.tokenlist = list()
		self.lineEnd = True
		self.filename = filename

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

		#TODO close fd

	def tokenize(self, line):
		line = line.strip()
		lineEndOld = self.lineEnd

		if line.endswith(';'):
			line = line.rstrip(';')
			tmptokenlist = line.split()
			self.lineEnd = True
		elif line.endswith(','):
			#line = line.rstrip(',')
			tmptokenlist = line.split()
			self.lineEnd = False
		else:
			tmptokenlist = line

		if lineEndOld:
			self.tokenlist = tmptokenlist
		else:
			self.tokenlist = self.tokenlist + tmptokenlist


	def makeStrOfTokens(self, start, tokenlist):
		tmplist = list()
		tmpstr = str()
		twoPortLists = False	#TODO shorten it!

		for i in xrange(start, len(tokenlist)):
			lokalelement = tokenlist.pop()

			if lokalelement.endswith(')') and lokalelement.startswith('(') and not twoPortLists:
				twoPortLists = True
				tmpstr = lokalelement
			elif lokalelement.endswith(')') and lokalelement.startswith('(') and twoPortLists:
				tmplist.append(tmpstr)
				tmpstr = lokalelement
			elif lokalelement.endswith(')') and twoPortLists:
				tmplist.append(tmpstr)
				tmpstr = ''
				tmpstr = tmpstr + lokalelement
			elif lokalelement.endswith(')') and not twoPortLists:
				twoPortLists = True
				tmpstr = tmpstr + lokalelement
			elif lokalelement.endswith(','):
				tmpstr = lokalelement + tmpstr
			elif lokalelement.startswith('('):
				tmpstr = lokalelement + tmpstr
			else:
				tmpstr = lokalelement

		tmplist.append(tmpstr)
		tmplist.reverse()
		return tokenlist + tmplist

	def interpretLine(self, line):
		if line.startswith('//'):
			return

		self.tokenize(line)
		if not self.lineEnd:
			return

		if isinstance(self.tokenlist, list):
			if not(self.tokenlist[0] == 'input' or self.tokenlist[0] == 'output' or self.tokenlist[0] == 'wire' or self.tokenlist[0] == 'reg'):
				tmptokenlist = self.makeStrOfTokens(2, self.tokenlist)
				tmpPortList = self.makeList(tmptokenlist[2])
			else:
				tmptokenlist = self.makeStrOfTokens(1, self.tokenlist)

		if self.tokenlist[0] == 'module':
			++self.moduleNumber
			self.modulelist.append(VerilogModule(tmptokenlist[1], tmpPortList))
		elif self.tokenlist[0] == 'and':
			self.modulelist[self.moduleNumber].addGate(AND(tmptokenlist[1], tmpPortList))
		elif self.tokenlist[0] == 'or':
			self.modulelist[self.moduleNumber].addGate(OR(tmptokenlist[1], tmpPortList))
		elif self.tokenlist[0] == 'nand':
			self.modulelist[self.moduleNumber].addGate(NAND(tmptokenlist[1], tmpPortList))
		elif self.tokenlist[0] == 'nor':
			self.modulelist[self.moduleNumber].addGate(NOR(tmptokenlist[1], tmpPortList))
		elif self.tokenlist[0] == 'xor':
			self.modulelist[self.moduleNumber].addGate(XOR(tmptokenlist[1], tmpPortList))
		elif self.tokenlist[0] == 'not':
			self.modulelist[self.moduleNumber].addGate(NOT(tmptokenlist[1], tmpPortList))
		elif self.tokenlist[0] == 'buf':
			None
			#self.modulelist[self.moduleNumber].addBranch(XOR(tmptokenlist[1], tmpPortList))
		elif self.tokenlist == 'endmodule':
			self.modulelist[self.moduleNumber].setEnd()
		else:
			self.modulelist[self.moduleNumber].addGate((tmptokenlist[0], self.makeList(tmptokenlist[1])))

	def makeList(self, ports):
		tmplist = ports.rstrip(')')
		tmplist = tmplist.lstrip('(')
		tmplist = tmplist.replace(' ','')
		return tmplist.split(',')

	def checkSyntax():
		for i in xrange(len(modulelist)):
			if not modulelist[i].getEnd():
				return False

			branchList = modulelist[i].getBranchList()
			#TODO: check for syntax error
		return True

	def insertModules(self):
		modListTop = list()
		modListBottom = list()


		for i in xrange(len(modulelist)):
			modList.append((modulelist[i].getName(), i))

			branchList = modulelist[i].getBranchList()
#			for n in range(0, --len(branchList)):
#				if branchList[n]:
#					modListBottom.append((
