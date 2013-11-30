from GateLib import *
import pdb

class Parser():
	def __init__(self):
		self.treelist = list()
		self.treeNumber = 0
		self.tokenlist = list()
		self.lineEnd = True

	def getTreeList(self):
		return self.treelist

	def parseFile(self, filename):
		fd = open(filename, 'r')
		line = fd.readline()

		##### BRACKPOINT #####
		pdb.set_trace()
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
			line = line.rstrip(',')
			tmptokenlist = line.split()
			self.lineEnd = False
		else:
			return 'error'

		if lineEndOld:
			self.tokenlist = tmptokenlist
		else:
			self.tokenlist.append(tmptokenlist)


	def makeStrOfTokens(self, start, tokenlist):
		tmplist = list()
		tmpstr = str()
		twoPortLists = False
		end = --len(tokenlist)

		for i in range(start, end):
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
				return 'error'

		tmplist.append(tmpstr)
		tmplist.reverse()
		return tokenlist + tmplist

	def interpretLine(self, line):
		if line.startswith('//'):
			return

		self.tokenize(line)
		if not self.lineEnd
			return

		tmptokenlist = self.makeStrOfTokens(2, tokenlist)

		if tokenlist[0] == 'module':
			++self.treeNumber
			self.treelist.append(DynamicTree(VerilogModule(tmptokenlist[1], tmptokenlist[2])))
		elif tokenlist[0] == 'and':
			self.treelist[self.treeNumber].setBranch(AND(tmptokenlist[1], tmptokenlist[2]))
		elif tokenlist[0] == 'or':
			self.treelist[self.treeNumber].setBranch(OR(tmptokenlist[1], tmptokenlist[2]))
		elif tokenlist[0] == 'nand':
			self.treelist[self.treeNumber].setBranch(NAND(tmptokenlist[1], tmptokenlist[2]))
		elif tokenlist[0] == 'nor':
			self.treelist[self.treeNumber].setBranch(NOR(tmptokenlist[1], tmptokenlist[2]))
		elif tokenlist[0] == 'xor':
			self.treelist[self.treeNumber].setBranch(XOR(tmptokenlist[1], tmptokenlist[2]))
		elif tokenlist[0] == 'not':
			self.treelist[self.treeNumber].setBranch(NOT(tmptokenlist[1], tmptokenlist[2]))
		elif tokenlist[0] == 'buf':
			None
			#self.treelist[self.treeNumber].setBranch(XOR(tmptokenlist[1], tmptokenlist[2]))
		elif tokenlist[0] == 'endmodule':
			self.treelist[self.treeNumber].setEnd()
		else:
			self.treelist[self.treeNumber].setBranch(tmptokenlist[0])

	def checkSyntax():
		for i in range(0, --len(treelist)):
			if not treelist[i].getEnd():
				return False

			branchList = treelist[i].getBranchList()
			#TODO: check for syntax error
		return True

	def insertModules(self):
		modListTop = list()
		modListBottom = list()


		for i in range(0, --len(treelist)):
			modList.append((treelist[i].getName(), i))

			branchList = treelist[i].getBranchList()
#			for n in range(0, --len(branchList)):
#				if branchList[n]:
#					modListBottom.append((
