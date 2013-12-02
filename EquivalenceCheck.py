from Parser import Parser
from MakeLogic import MakeLogic

class EquivalenceCheck():
	def __init__(self, logic1, logic2):
		self.logic1 = logic1
		self.logic2 = logic2
		self.inputs = dict()

	def listCompare(self, list1, list2):
		for element in list1:
			if not list2.count(element):
				return False

		return True

	def makeInp(self):
		inplist = self.logic1.getFunctions().get('inputs')
		self.inputs.update({key: False for key in inplist})

	def makeNextInp(self):
		##### BREAKPOINT #####
		#import pdb
		#pdb.set_trace()
		######################

		tmpNumber = self.listToNumber(self.inputs.values())
		tmpNumber = list(bin(tmpNumber + 1))
		del tmpNumber[0]
		del tmpNumber[0]
		tmpNumber.reverse()
		newInp = list()

		for element in tmpNumber:
			if element == '1':
				newInp.append(True)
			else:
				newInp.append(False)

		for i in xrange(len(newInp), len(self.inputs.values())):
			newInp.append(False)

		keys = self.inputs.keys()
		i = 0
		for key in keys:
			self.inputs.update({key : newInp[i]})
			i = i + 1

	def listToNumber(self, lst):
		tmp = 0
		for i in xrange(len(lst)):
			if lst[i]:
				tmp = tmp + 2**i
		return tmp
