import GateLib
import pdb

class Parser():
	def __init__(self):
		self.treelist = list()
		self.treeNumber = 0
#		tokenlists = list()
#		tokenNumber = 0

	def getTreeList(self):
		return self.treelist

	def parseFile(self, filename):
		fd = open(filename, r)
		line = fd.readline()

		while line:
			interpretLine(line)
			line = fd.readline()

		return True

	def tokenize(self, line):
		tokenlists = list()

		if line.endswith(';'):
			line = line.rstrip(';')
			if line.find(';') != -1:
				cmdlist = line.split(';')
				i = 0
				cmd = cmdlist[i]
				while cmd:
					++tokenNumber


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
		tokenlist = self.tokenize(line)

		for i in range(0,--len(tokenlist)):
			if tokenlist[i][0] == '\\':
				none
			elif tokenlist[i][0] == 'module':
#				++treeNumber
				tmptokenlist = makeStrOfTokens(1, tokenlist[i])
				self.treelist.append(DynamicTree(VerilogModule(tmptokenlist[1], tmptokenlist[0])))#tokenlist[i][1], tokenlist[i][2]))
			elif tokenlist[i][0] == 'input':
				self.treelist[self.treeNumber].setBranch(PortList('input' ,tokenlist[i][1]))
			elif tokenlist[i][0] == 'output':
				self.treelist[self.treeNumber].setBranch(PortList('output', tokenlist[i][1]))
			elif tokenlist[i][0] == 'wire':
				self.treelist[self.treeNumber].setBranch(PortList('wire', tokenlist[i][1]))
			elif tokenlist[i][0] == 'reg':
				self.treelist[self.treeNumber].setBranch(PortList('reg', tokenlist[i][1]))
			elif tokenlist[i][0] == 'and':
				self.treelist[self.treeNumber].setBranch(AND(tokenlist[i][1], tokenlist[i][2], tokenlist[i][3]))
			elif tokenlist[i][0] == 'or':
				self.treelist[self.treeNumber].setBranch(OR(tokenlist[i][1], tokenlist[i][2], tokenlist[i][3]))
			elif tokenlist[i][0] == 'nand':
				self.treelist[self.treeNumber].setBranch(NAND(tokenlist[i][1], tokenlist[i][2], tokenlist[i][3]))
			elif tokenlist[i][0] == 'nor':
				self.treelist[self.treeNumber].setBranch(NOR(tokenlist[i][1], tokenlist[i][2], tokenlist[i][3]))
			elif tokenlist[i][0] == 'xor':
				self.treelist[self.treeNumber].setBranch(XOR(tokenlist[i][1], tokenlist[i][2], tokenlist[i][3]))
			elif tokenlist[i][0] == 'endmodule':
				self.treelist[self.treeNumber].setEnd()
			else:
				self.treelist[self.treeNumber].setBranch(tokenlist[i][0])

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
