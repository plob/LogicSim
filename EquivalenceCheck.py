from Parser import Parser
from MakeLogic import MakeLogic
from copy import copy
from os import fork
from os import _exit
from os import waitpid

class EquivalenceCheck():
	def __init__(self, logic1, logic2):
		self.logic1 = logic1.getFunctions()
		self.logic2 = logic2.getFunctions()

		if not self.listCompare(self.logic1.get('inputs').keys(), self.logic2.get('inputs').keys()):
			return 'Inputs are not equal!'
		self.inputs = copy(self.logic1.get('inputs'))

		self.outputs1 = copy(self.logic1.get('outputs'))
		self.outputs2 = copy(self.logic2.get('outputs'))
		if not self.listCompare(self.outputs1.keys(), self.outputs2.keys()):
			return 'Outputs are not equal!'

#		self.makeInp()
#		self.makeOut()

	def listCompare(self, list1, list2):
		for element in list1:
			if not list2.count(element):
				return False

		return True

	def makeInp(self):
		##### BREAKPOINT #####
		#import pdb
		#pdb.set_trace()
		######################
		inplist = self.logic1.get('inputs')
		if not self.listCompare(inplist, self.logic2.get('inputs')):
			return 'Inputs not equal!'
		self.inputs.update({key: False for key in inplist})

	def makeOut(self):
		outplist = self.logic1.get('outputs')
		if not self.listCompare(outplist, self.logic2.get('outputs')):
			return 'Outputs not equal!'
		self.outputs1.update({key: False for key in outplist})
		self.outputs2 = copy(self.outputs1)

	def makeNextInp(self):
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

		keys = self.inputs.keys() #TODO: insure cosistent order of the revcieved list
		i = 0
		for key in keys:
			self.inputs.update({key : newInp[i]})
			i = i + 1

	def generateOutputs(self):
		inpForLogic1 = dict()
		inpForLogic2 = dict()

		for outp in self.outputs1.keys():
			inpForLogic1.update({outp : self.generateArg(self.logic1.get(outp)[1])})
			inpForLogic2.update({outp : self.generateArg(self.logic2.get(outp)[1])})

		for outp in self.outputs1.keys():
			self.outputs1.update({outp : self.logic1.get(outp)[0](inpForLogic1.get(outp))})
			self.outputs2.update({outp : self.logic2.get(outp)[0](inpForLogic2.get(outp))})

	def compareLogic(self):
		inpnum = len(self.inputs.keys())
		divBy4 = 2**inpnum/4
		pid1 = fork()
		if not pid1:
			pid2 = fork()
			if not pid2:
				pid3 = fork()
				if not pid3:
					print 'last child'
					for i in xrange(3*divBy4, 4*divBy4):
						self.generateOutputs()
						for outp in self.outputs1.keys():
							if not (self.outputs1.get(outp) == self.outputs2.get(outp)):
								print 'False'
								t1 = False
								_exit(0)
					print 'True'
					t1 = True
					_exit(0)
				else:
					print 'parent: ' + str(pid3)
					for i in xrange(2*divBy4, 3*divBy4):
						self.generateOutputs()
						for outp in self.outputs1.keys():
							if not (self.outputs1.get(outp) == self.outputs2.get(outp)):
								print 'False'
								t2 = False
								_exit(0)
					print 'True'
					_exit(0)
					waitpid(pid3, 0)
					t2 = True
			else:
				print 'grandparent: ' + str(pid2)
				for i in xrange(divBy4, 2*divBy4):
					self.generateOutputs()
					for outp in self.outputs1.keys():
						if not (self.outputs1.get(outp) == self.outputs2.get(outp)):
							print 'False'
							t3 = False
							_exit(0)
				print 'True'
				t3 = True
				waitpid(pid3, 0)
				waitpid(pid2, 0)
				_exit(0)
		else:
			print 'grandgrandparent: ' + str(pid1)
			for i in xrange(0, divBy4):
				self.generateOutputs()
				for outp in self.outputs1.keys():
					if not (self.outputs1.get(outp) == self.outputs2.get(outp)):
						print 'False'
						t4 = False
			print 'True'
			t4 = True
			waitpid(pid1, 0)
			waitpid(pid2, 0)
			waitpid(pid3, 0)

		return t1 and t2 and t3 and t4

	def generateArg(self, pattern):
		newarg = list()

		for i in xrange(len(pattern)):
			if isinstance(pattern[i], list):
				newarg.append(self.generateArg(pattern[i]))
			else:
				newarg.append(self.inputs.get(pattern[i]))

		return newarg

	def listToNumber(self, lst):
		tmp = 0
		for i in xrange(len(lst)):
			if lst[i]:
				tmp = tmp + 2**i
		return tmp
