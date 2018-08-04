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

import os
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

		sources = [x.strip().lower() for x in open(self.projectFile).readlines() if x.strip() != ""]
		target = None
		for src in [x for x in sources if x.find("//") < 0 and x.find("=") >= 0]:
			equ = [x.strip() for x in src.split("=") if x.strip() != ""]
			if equ[0] == "output":
				target = equ[1]

		for src in [x for x in sources if x.find("//") < 0 and x.find("=") < 0]:
			print("M13:Building "+src)
			self.compiler.compileFile(src)
		if target is None:
			target = "object"

		self.binary.save("build"+os.sep+target+".m13",self.dictionary)
		self.dictionary.save("build"+os.sep+target+".dictionary")
		print("M13Binary:Completed build of "+target+".m13")

