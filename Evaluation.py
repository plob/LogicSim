from GateLib import *

class Evaluation():
	def __init__(self, parserObj):
		self.moduleList = parserObj.getModuleList()

	def ABC(self):
		for i in xrange(len(self.moduleList)):
			#TODO

	def makeEquation(self, number):
		gateList = self.moduleList[number].getGateList()
		for i in xrange(len(gateList)):


