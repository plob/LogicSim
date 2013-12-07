from GateLib import *
#from sys import close

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

	def tokenize(self, line):	#TODO may implement makeStrOfTokens here
		line = line.strip()		#would be nice, look down there for hints
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
		twoPortLists = False	#TODO shorten it! its old and way to long
								#TODO make it to split the name from the port list if not devided by a space
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
			self.moduleNames.update({tmtokenlist[1] : self.moduleNumber})
			self.modulelist.append(VerilogModule(tmptokenlist[1], tmpPortList))
			self.moduleNumber = self.moduleNumber + 1
		elif self.tokenlist[0] == 'and':
			self.modulelist[self.moduleNumber - 1].addGate(AND(tmptokenlist[1], tmpPortList))
		elif self.tokenlist[0] == 'or':
			self.modulelist[self.moduleNumber - 1].addGate(OR(tmptokenlist[1], tmpPortList))
		elif self.tokenlist[0] == 'nand':
			self.modulelist[self.moduleNumber - 1].addGate(NAND(tmptokenlist[1], tmpPortList))
		elif self.tokenlist[0] == 'nor':
			self.modulelist[self.moduleNumber - 1].addGate(NOR(tmptokenlist[1], tmpPortList))
		elif self.tokenlist[0] == 'xor':
			self.modulelist[self.moduleNumber - 1].addGate(XOR(tmptokenlist[1], tmpPortList))
		elif self.tokenlist[0] == 'xnor':
			None #never have seen it, but may some where in the future
		elif self.tokenlist[0] == 'not':
			self.modulelist[self.moduleNumber - 1].addGate(NOT(tmptokenlist[1], tmpPortList))
		elif self.tokenlist[0] == 'buf':
			None #never have seen it, but may some where in the future
		elif self.tokenlist == 'endmodule':
			self.modulelist[self.moduleNumber - 1].setEnd()
		else:
			self.modulelist[self.moduleNumber - 1].addGate((tmptokenlist[0], self.makeList(tmptokenlist[1])))

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
			#for module in modulelist:
			#	for name in moduleNames.keys():
			#		if module.hasModule(name):
			#			gateList = modulelist[moduleNames.get(name)].getGateList()
			#			module.substitudeModule(name, gateList)

		return None
