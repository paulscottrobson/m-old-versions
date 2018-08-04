# ****************************************************************************************
# ****************************************************************************************
#
#		Name:		createdictionary.py
#		Purpose:	Create dictionary for words identified in .lst file
#		Date:		24th July 2018
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ****************************************************************************************
# ****************************************************************************************

import re

words = {} 														# scan .vice file 
#
#		Get the lines of the label listing file that are word definition beginnings.
#
listFile = [x for x in open("system.bin.vice").readlines()]		# read it in and tidy up.
listFile = [x.strip().upper() for x in listFile if x.strip() != ""]
listFile = [x for x in listFile if x.find("WORD_DEF") > 0]		# extract the labels
listFile = [x for x in listFile if x.find("END_WORD_DEF") < 0]
#
#		Scan them and convert to a useable format
#
for l in listFile:
	m = re.match("^AL\s*C\:([0-9A-F]+)\s*_(.*)$",l)				# strip information out
	assert m is not None,"Can't parse '{0}'".format(l)
	name = m.group(2)											# convert it
	address = int(m.group(1),16)
	if name[:10] == "WORD_DEF__":								# M12 word definition (code word/macro)
		m = re.match("^([A-Z]+)_([0-9A-F_]+)",name[10:])		# analyse the name
		assert m is not None,"Bad name '{0}'".format(name)
		assert m.group(1) == "WORD" or m.group(1) == "MACRO","Bad type in '{0}'".format(name)
		wordName = m.group(2).split("_")						# convert name back from ASCII to text
		wordName = "".join([chr(int(x,16)) for x in wordName])
																# add to the list.
		words[wordName] = {"name":wordName,"type":m.group(1).lower(),"address":address}
	else:
		assert False,"???? "+l
#
#		Write out the dictionary information.
#
wordList = [x for x in words.keys()]							# get a list
wordList.sort(key = lambda x:words[x]["address"]) 				# sort it in address order.
h = open("core.dictionary","w")
for w in wordList:
	h.write("{0:04x}::{1}::{2}\n".format(words[w]["address"],words[w]["type"].lower(),w))
h.close()
print("Built core.dictionary")
