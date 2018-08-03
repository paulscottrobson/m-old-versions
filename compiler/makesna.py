#
#	Create an SNA file.
#
def createSNA(prefix):
	snaCode = """
	#target sna

	#code HEAD, 0, 27
	        defb    $3f             ; i
	        defw    0               ; hl'
	        defw    0               ; de'
	        defw    0               ; bc'
	        defw    0               ; af'

	        defw    0               ; hl
	        defw    0               ; de
	        defw    0               ; bc
	        defw    0               ; iy
	        defw    0               ; ix

	        defb    0<<2            ; bit 2 = iff2 (iff1 before nmi) 0=di, 1=ei
	        defb    0,0,0           ; r,f,a
	        defw    stackend        ; sp
	        defb    1               ; irpt mode
	        defb    1              ; border color: 0=black ... 7=white

	#code SLOW_RAM, 0x4000, 0xC000

	pixels_start:   defs 0x1800
	attr_start:     defs 0x180

	stackbot:   defs    0x3e
	stackend:   defw    0x5A00  ; will be popped into pc when the emulator loads the .sna file
	        
	        org     $5A00
	code_start:
	        jp      $5B00
	        org     $5B00
	        incbin  "{0}.m13"
	""".format(prefix).split("\n")
	snaCode = "\n".join([x[1:] for x in snaCode])
	h = open("__"+prefix+".asm","w")
	h.write(snaCode+"\n\n")
	h.close()
#
#		Create run.shand buid.sh
#
def GenerateScripts(prefix):
	buildCode = """
		cd ../core.build
		sh build.bat
		cd ../compiler
		rm {0}.bin {0}.sna
		python ../compiler/m13c.py
		zasm -bu __{0}.asm
	""".format(prefix)
	buildCode = [x.lstrip() for x in buildCode.split("\n") if x.strip() != ""]
	h = open("build.sh","w").write("\n".join(buildCode))
	#
	runCode = """
		rm {0}.sna
		sh build.sh
		fuse --debugger-command "br 0x5B00" __{0}.sna 2>/dev/null
	""".format(prefix)
	runCode = [x.lstrip() for x in runCode.split("\n") if x.strip() != ""]
	h = open("run.sh","w").write("\n".join(runCode))
	

prefix = "test"
createSNA(prefix)
GenerateScripts(prefix)
