from GateLib import *
from Parser import Parser
from copy import copy
import subprocess

class MakeSAT():
	def __init__(self, parserObj1, parserObj2, pathToMinisat = 'minisat'):
		self.moduleList1 = parserObj1.getModuleList()
		self.moduleList2 = parserObj2.getModuleList()
		self.gateList1 = self.moduleList1[0].getGateList()
		self.gateList2 = self.moduleList2[0].getGateList()
		self.compareCircuit = list()
		self.pathToMinisat = pathToMinisat
		self.pinToNumber1 = dict()
		self.pinToNumber2 = dict()
		self.outputs = list()
		numI = self.makePortNumberRelations()
		self.makeCompareCircuit(numI)

	def makeCompareCircuit(self, i):
		outpXOR = list()

		for outp in self.outputs:
			self.compareCircuit.append(XOR('XOR_' + outp, ['X_' + outp, outp, outp]))
			self.pinToNumber1.update({'X_' + outp : i})
			self.pinToNumber2.update({'X_' + outp : i})
			outpXOR.append('X_' + outp)
			i = i + 1

		if len(outpXOR) > 1:
			self.compareCircuit.append(OR('OR_Final', ['OR_Final_Output',] + outpXOR ))
			self.pinToNumber1.update({'OR_Final_Output' : i})
			self.pinToNumber2.update({'OR_Final_Output' : i})

	def makePortNumberRelations(self):
		##### BREAKPOINT #####
		#import pdb
		#pdb.set_trace()
		######################
		i = 1
		for item in copy(self.gateList1):
			if isinstance(item, tuple):
				if item[0] == 'input':
					inputs1 = item[1]
					self.gateList1.remove(item)
				elif item[0] == 'output':
					outputs1 = item[1]
					self.gateList1.remove(item)
				elif item[0] == 'wire':
					wires1 = item[1]
					self.gateList1.remove(item)
				else:
					None
			else:
				break

		for item in copy(self.gateList2):
			if isinstance(item, tuple):
				if item[0] == 'input':
					inputs2 = item[1]
					self.gateList2.remove(item)
				elif item[0] == 'output':
					outputs2 = item[1]
					self.gateList2.remove(item)
				elif item[0] == 'wire':
					wires2 = item[1]
					self.gateList2.remove(item)
				else:
					None
			else:
				break

		if not self.listsEqual(inputs1, inputs2):
			return 'error'
		if not self.listsEqual(outputs1, outputs2):
			return 'error'
		self.outputs = outputs1

		for inp in inputs1:
			self.pinToNumber1.update({inp : i})
			self.pinToNumber2.update({inp : i})
			i = i + 1

		for outp in outputs1:
			self.pinToNumber1.update({outp : i})
			i = i + 1
			self.pinToNumber2.update({outp : i})
			i = i + 1

		try:
			for wire in wires1:
				self.pinToNumber1.update({wire : i})
				i = i + 1
		except UnboundLocalError:
			None

		try:
			for wire in wires2:
				self.pinToNumber2.update({wire : i})
				i = i + 1
		except UnboundLocalError:
			None

		return i


	def listsEqual(self, list1, list2):
		for element in list1:
			if not list2.count(element):
				return False
		return True

	def useMinisat(self):
		minisat = subprocess.Popen(self.pathToMinisat, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, stdin = subprocess.PIPE)
		pipeToMinisat = minisat.stdin.writelines
		pipeFromMinisat = minisat.communicate
#		fd = open('outputs_test', 'w')
#		pipeToMinisat = fd.writelines

#		print minisat.stdout.read(1)

		for gate in self.gateList1:
			clauses = gate.makeClauses(self.pinToNumber1)
			for clause in clauses:
				print clause
				pipeToMinisat(clause + '\n')

		for gate in self.gateList2:
			clauses = gate.makeClauses(self.pinToNumber2)
			for clause in clauses:
				print clause
				pipeToMinisat(clause + '\n')

		for gate in self.compareCircuit:
			if isinstance(gate, XOR):
				clauses = gate.makeClauses2(self.pinToNumber1, self.pinToNumber2)
				lastOutp = self.pinToNumber1.get(gate.getOutp())
			else:
				clauses = gate.makeClauses(self.pinToNumber1)
				lastOutp = self.pinToNumber1.get(gate.getOutp())

			for clause in clauses:
				print clause
				pipeToMinisat(clause + '\n')

		print `lastOutp` + ' 0\n'
		pipeToMinisat(`lastOutp` + ' 0\n')
		pipeToMinisat('ctrl-D')
#		fd.close()

		print pipeFromMinisat()[0].decode('string_escape')
