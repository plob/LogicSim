from GateLib import *

class Evaluation():
	def __init__(self, parserObj):
		self.moduleList = parserObj.getModuleList()
		self.outpFuncRel = dict()
		self.ioPortRel = dict()

#	def ABC(self):
#		for i in xrange(len(self.moduleList)):
			#TODO for more modules

	def makeRelations(self, number):
		gateList = self.moduleList[number].getGateList()
		for element in gateList:
			if isinstance(element, GATE):
				gateoutp = element.getOutp()

				self.outpFuncRel.update({gateoutp : element.outpFunc})
				self.ioPortRel.update({gateoutp : element.getInp()})
			elif element[0] == 'output':
				self.output = {key: False for key in element[1]}
			elif element[0] == 'input':
				self.inputs = {key: False for key in element[1]}

	def makeFunctions(self):
		##### BREAKPOINT #####
		#import pdb
		#pdb.set_trace()
		######################

		for key in self.ioPortRel:
			inplist = copy(self.ioPortRel.get(key))

			for inp in inplist:
				tmp = inplist.pop()
				if not self.inputs.has_key(tmp):
					newfunc = self.concatFunc(self.outpFuncRel.get(key), self.outpFuncRel.get(tmp))
					self.outpFuncRel.update({key : newfunc})
					self.ioPortRel.update({key : inplist + self.ioPortRel.get(tmp)})
				else:
					inplist.insert(0, tmp)

	def concatFunc(self, func1, func2):
		def tmpfunc(arg):
			##### BREAKPOINT #####
			#import pdb
			#pdb.set_trace()
			######################
			tmp = func2(arg)
			tmp = func1(tmp)
			return tmp

		return tmpfunc

	def getOutpFunctions(self)
		tmpList = dict()
		for i in copy(self.output):
			tmpList.update({i : (self.outpFuncRel.get(i), self.ioPortRel.get(i))})

		return tmpList
