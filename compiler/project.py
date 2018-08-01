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


# ****************************************************************************************
#									Project class
# ****************************************************************************************

class Project(object):
	def __init__(self,projectFile):
		self.projectFile = projectFile

	def build(self):
		self.dictionary = Dictionary()
		self.binary = M12Binary(self.dictionary)
		self.compiler = Compiler(self.binary,self.dictionary)
		sources = [x.strip() for x in open(self.projectFile).readlines() if x.strip() != ""]
		for src in [x for x in sources if x.find("//") < 0]:
			print("M12:Building "+src)
			self.compiler.compileFile(src)
		self.dictionary.createDictionary(self.binary)
		self.binary.save()
		print("M12Binary:Completed.")

