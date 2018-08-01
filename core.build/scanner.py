#
#		Build words.asm and macros.asm
#
import os,re
#
#		Get a sorted list of all sourcefiles
#
sourceFiles = []
for root,dirs,files in os.walk("../core.dictionary"):
	for f in files:
		sourceFiles.append(root+os.sep+f)
sourceFiles = [s for s in sourceFiles if s[-4:] == ".src"]
sourceFiles.sort()
#
#		Read in each source file
#
sources = {}
for f in sourceFiles:
	code = [x.rstrip() for x in open(f).readlines()]
	word = ""
	wtype = ""
	for c in code:
		if c.find("@name") > 0:
			m = re.match("^\s*\;\s*\@name\s*(.*)$",c)
			assert m is not None,"Bad line "+c
			word = m.group(1)
		if c.find("@type") > 0:
			m = re.match("^\s*\;\s*\@type\s*(.*)$",c)
			assert m is not None,"Bad line "+c
			wtype = m.group(1)

	code = [x.replace("\t","    ") for x in code if x != "" and x[0] != ";"]
#	print(">>>>>>",word,wtype)
#	print("\n".join(code))

	newSource = { "name":word, "type": wtype, "code":code }
	if wtype == "word" and code[-1].strip() != "ret":
		print("Warning, word {0} has no terminating ret".format(word))
	sources[f] = newSource

for typeGroup in ["macro","word"]:
	print("Building asm"+os.sep+typeGroup+".asm")
	h = open("asm"+os.sep+typeGroup+".asm","w")
	h.write("; **** generated by scanner.py ****\n\n")
	keys = [x for x in sources.keys() if sources[x]["type"] == typeGroup]
	keys.sort()
	for k in keys:
		h.write("\n; ***** {0} *****\n\n".format(sources[k]["name"]))
		label = ["{0:02x}".format(ord(x)) for x in sources[k]["name"]]
		label = "word_def__"+typeGroup+"_"+"_".join(label)
		h.write(label+":\n")
		if typeGroup == "macro":
			h.write("        ld a,end_{0}-{0}-3-2\n".format(label))
			h.write("        call MacroExpander\n")
		h.write("\n".join(sources[k]["code"]))
		h.write("\n")
		if typeGroup == "macro":
			h.write("end_"+label+":\n")
	h.close()
print("Done.")