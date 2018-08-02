# ****************************************************************************************
# ****************************************************************************************
#
#		Name:		project.py
#		Purpose:	M13 Project Manager
#		Date:		1st August 2018
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ****************************************************************************************
# ****************************************************************************************

from dictionary import *
from binary import *
from compiler import *

# ****************************************************************************************
#									Project class
# ****************************************************************************************

class Project(object):
	def __init__(self,projectFile):
		self.projectFile = projectFile

	def build(self):
		self.dictionary = Dictionary("core.dictionary")
		self.binary = M13Binary(self.dictionary,"core.m13")
		self.compiler = Compiler(self.binary,self.dictionary)
		sources = [x.strip() for x in open(self.projectFile).readlines() if x.strip() != ""]
		for src in [x for x in sources if x.find("//") < 0]:
			print("M13:Building "+src)
			self.compiler.compileFile(src)
		self.binary.save("test.m13",self.dictionary)
		self.dictionary.save("test.dictionary")
		print("M13Binary:Completed.")

