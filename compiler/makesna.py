# ****************************************************************************************
# ****************************************************************************************
#
#		Name:		makesna.py
#		Purpose:	Create assembler skeleton for SNA and Batch Files.
#		Date:		1st August 2018
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ****************************************************************************************
# ****************************************************************************************

import os,sys
#
#	Create an SNA file.
#
def createSNA(prefix):
	snaCode = """
		opt 	zxNext        
        org     $5B00
        incbin  "build\\{0}.m13"
        savesna "build\\__{0}.sna",$5B00
	""".format(prefix).split("\n")
	snaCode = "\n".join([x[1:] for x in snaCode])
	h = open("build"+os.sep+"__"+prefix+".asm","w")
	h.write(snaCode+"\n\n")
	h.close()
#
#		Create run.shand buid.sh
#
def GenerateScripts(prefix):
	buildCode = """
		@echo off
		pushd ..\\core.build
		call build.bat
		popd
		python ..\\compiler\\m13c.py
		..\\bin\\snasm -zxnext -brk -cur build\\__{0}.asm
	""".format(prefix)
	buildCode = [x.lstrip() for x in buildCode.split("\n") if x.strip() != ""]
	h = open("build.bat","w").write("\n".join(buildCode))
	#
	runCode = """
		@echo off
		call build.bat
		..\\bin\\cspect.exe -zxnext -brk build\\__{0}.sna
	""".format(prefix)
	runCode = [x.lstrip() for x in runCode.split("\n") if x.strip() != ""]
	h = open("run.bat","w").write("\n".join(runCode))
	

if len(sys.argv) == 1:
	print("python makesna.py <build stub>")
else:
	prefix = sys.argv[1]
	if not os.path.isdir("build"):
		os.mkdir("build")
	createSNA(prefix)
	GenerateScripts(prefix)
