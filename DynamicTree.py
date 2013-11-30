class DynamicTree:
#	def __init__(self):
#		self.branches = 0
#		self.branchPointer = 0
#		self.node = none
#		self.branchList = list()

	def __init__(self, nodeObj):
		self.branches = 0
		self.branchPointer = 0
		self.node = nodeObj
		self.branchList = list()

	def setBranch(self, obj):
		self.branchList.append(obj)
		++branchPointer

	def getNode(self):
		return self.node

	def getBranchList(self):
		return self.branchList
