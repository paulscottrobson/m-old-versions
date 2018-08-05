# ****************************************************************************************
# ****************************************************************************************
#
#		Name:		importdict.py
#		Purpose:	Import dictionary into .m13 file (or display it)
#		Date:		5th August 2018
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ****************************************************************************************
# ****************************************************************************************

import os,sys

class DictionaryWorker(object):
	def __init__(self):
		self.loadAddress = 0x5B00
	#
	#		Load files and basic info
	#
	def loadBasic(self,coreFile,dictFile):
		self.binary = [0x00] * 0x10000
		h =  open(coreFile,"rb")
		coreBinary = [x for x in h.read(-1)]
		h.close()
		self.size = len(coreBinary)
		for i in range(0,len(coreBinary)):
			self.binary[self.loadAddress+i] = coreBinary[i]
		self.wordList = [x.strip().upper() for x in open(dictFile).readlines()]
		self.sysInfo = None
		for w in self.wordList:
			if w[-8:] == "SYS.INFO":
				self.sysInfo = int(w[:4],16)
		assert self.sysInfo is not None
		print("sys.info is at ${0:04x}".format(self.sysInfo))
		self.dictBase = self.binary[self.sysInfo+4]+self.binary[self.sysInfo+5] * 256
		print("dictionary is at ${0:04x}".format(self.dictBase))
	#
	#		Import dictionary
	#
	def importDictionary(self,coreFile,dictFile):
		self.loadBasic(coreFile,dictFile)
		p = self.dictBase
		for w in self.wordList:
			w = w.split("::")
			address = int(w[0],16)
			self.write(p+0,len(w[2]) + 5)							# offset + 0 : offset to next (0 = End)
			self.write(p+1,address & 0xFF)							# offset + 1 : LSB of routine address
			self.write(p+2,address >> 8)							# offset + 2 : MSB of routine address
			self.write(p+3,0)										# offset + 3 : page of routine
			self.typeID = len(w[2])									# offset + 4 : Bits 0..4 length of word name
			self.typeID += (0x20 if w[1] == "variable" else 0x00)	# 			   Bit 5 marks as a variable
			self.typeID += (0x40 if w[1] == "immediate" else 0x00)	#			   Bit 6 marks as immediate
																	# 			   Bit 7 private flag for compaction
			self.write(p+4,self.typeID)								# offset + 5 : Name as 6 bit ASCII
			for c in range(0,len(w[2])):
				self.write(p+5+c,ord(w[2][c]) & 0x3F)
			p = p + len(w[2]) + 5 									# next
		self.write(p,0)												# dictionary end marker

		print("words output in dictionary {0}".format(len(self.wordList)))
		print("dictionary next free byte is ${0:04x}".format(p))
		for x in range(0,3):											# copy to actual pointer and copies.
			self.binary[self.sysInfo + 6 + x * 6] = p & 0xFF			
			self.binary[self.sysInfo + 7 + x * 6] = p >> 8

		h = open(coreFile,"wb")
		h.write(bytes(self.binary[0x5B00:0x5B00+self.size]))
		h.close()
	#
	def write(self,addr,data):
		c = chr((data ^ 0x20) + 0x20).lower()
		#print("{0:04x} : {1:02x} {2}".format(addr,data,c))
		self.binary[addr] = data
	#
	#		Display the dictionary
	#
	def exportDictionary(self,coreFile,dictFile):
		self.loadBasic(coreFile,dictFile)
		p = self.dictBase
		while self.binary[p] != 0:
			name = self.binary[p+5:p+5+(self.binary[p+4] & 0x1F)]
			name = [chr((x^0x20)+0x20) for x in name]
			name = "".join(name).lower()
			addr = self.binary[p+1] + self.binary[p+2] * 256
			type = "word" if (self.binary[p+4] & 0x20) == 0 else "var"
			type = type if (self.binary[p+4] & 0x40) == 0 else "imm"
			print("Dict at: ${0:04x} Addr:${2:04x} {3:4} {1}".format(p,name,addr,type))
			p += self.binary[p]


DictionaryWorker().importDictionary("core.m13","core.dictionary")
DictionaryWorker().exportDictionary("core.m13","core.dictionary")