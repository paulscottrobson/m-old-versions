# ****************************************************************************************
# ****************************************************************************************
#
#		Name:		compiler.py
#		Purpose:	M13 Compiler
#		Date:		1st August 2018
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ****************************************************************************************
# ****************************************************************************************

import sys,re
from exceptions import *

# ****************************************************************************************
#										Compiler class
# ****************************************************************************************

class Compiler(object):
	def __init__(self,binary,dictionary):
		self.binary = binary
		self.dictionary = dictionary
		Compiler.sourceFile = "<unknown>"
	#
	#		Compile a file
	#
	def compileFile(self,sourceFile):
		Compiler.sourceFile = sourceFile
		self.compileSource(open(sourceFile).readlines())
	#
	#		Compile an array of source
	#
	def compileSource(self,lines):
		Compiler.lineNumber = 1 									# error number
		for l in lines:												# work through source
			l = l if l.find("//") < 0 else l[:l.find("//")]			# remove comments
			for w in l.replace("\t"," ").strip().split(" "):		# scan through source
				if w != "":											# compile non blanks
					try:
						self.compileWord(w)
					except CompilerException as e:
						print("{0} line {1} of {2}".format(e,Compiler.lineNumber,Compiler.sourceFile))
						sys.exit(1)

			Compiler.lineNumber += 1								# advance line number
	#
	#		Compile a single word
	#
	def compileWord(self,word):
		word = word.lower()											# make LC
		if self.binary.echo:
			self.binary.listing.write(" -- {0} --\n".format(word))
		originalWord = word 										# save original Word

		if word[0] == ':' and len(word) > 1:						# :definition
			self.dictionary.add(word[1:].lower(),"word",self.binary.pointer)
			return
	
		# handle normal words
		entry = self.dictionary.find(word) 							# find entry.
		if entry is not None:
			if entry.getType() != "variable":
				self.generateWordCode(entry.getAddress(),entry.getType(),entry.getName())
			else:
				self.loadConstant(entry.getAddress())
			return
		# variable accessors
		if word[-1] == '!' or word[-1] == '@':
			entry = self.dictionary.find(word[:-1])
			if entry is not None:
				self.variableAccess(word[-1] == '!',entry.getAddress())
				return
		# decimal constants
		if re.match("^(\-?[0-9]+)$",word):							# 1234 handles ^
			self.loadConstant(int(word,10) & 0xFFFF)
			return
		# hexadecimal constants
		if re.match("^(\$[0-9a-f]+)$",word):						# $1234 handles ^
			self.loadConstant(int(word[1:],16) & 0xFFFF)
			return
		# string constants
		if len(word) > 1 and word[0] == '"' and word[-1] == '"':	# "hi" string constant
			self.loadStringConstant(word[1:-1])
			return

		# structures
		if word == "if" or word == "-if" or word == "then":
			if word == "if" or word == "-if":
				self.ifAddress = self.createBranch("+" if word == "-if" else "0")
			else:
				self.completeBranch(self.ifAddress,self.binary.pointer)
			return

		if word == "begin" or word == "until" or word == "-until":
			if word == "begin":
				self.beginAddress = self.binary.pointer
			else:
				addr = self.createBranch("+" if word == "-until" else "0")
				self.completeBranch(addr,self.beginAddress)
			return

		if word == "for" or word == "next" or word == "i":
			if word == "for":
				self.forAddress = self.binary.pointer
				self.binary.write(0x2B)								# dec hl
				self.binary.write(0xE5)								# push hl
			if word == "next":
				self.binary.write(0xE1)								# pop hl
				addr = self.createBranch("#")						# branch if non zero
				self.completeBranch(addr,self.forAddress)			# to here
			if word == "i":
				self.binary.write(0xE1)								# pop hl
				self.binary.write(0xE5)								# push hl
			return

		# others
		if word[:9] == "variable:":									# 2 byte variable
			self.dictionary.add(word[9:].lower(),"variable",self.binary.pointer)		
			self.binary.write2(0)
			self.dictionary.makeLastPrivate()
			return

		if word == "private":										# make last def private
			self.dictionary.makeLastPrivate()
			return
		if word == "immediate":										# make last def immediate
			self.dictionary.makeLastImmediate()
			return
		# give up
		raise CompilerException("Cannot understand "+originalWord)
	#
	#		Load Constants
	#
	def loadConstant(self,const):
		self.binary.write(0xEB)										# EX DE,HL
		self.binary.write(0x21)										# LD HL,nnnn
		self.binary.write2(const)
	#
	#		Load String Constants
	#
	def loadStringConstant(self,string):
		self.binary.write(0x18)
		self.binary.write(1+len(string))
		address = self.binary.pointer
		self.binary.write(len(string))
		string = [ord(x) & 0x3F for x in string.replace("_"," ").upper()]
		for c in string:
			self.binary.write(c)
		self.binary.write(0xEB)										# EX DE,HL
		self.loadConstant(address)
	#
	#		Create a branch instruction
	#
	def createBranch(self,test):
		if test == "+":												# branch if +ve
			self.binary.write(0xCB)									# bit 7,h
			self.binary.write(0x7C)
		else:														# branch if zero/nonzero.
			self.binary.write(0x7C)									# ld a,h
			self.binary.write(0xB5)									# or l
		self.binary.write(0x28 if test != "#" else 0x20)			# branch zero or non zero										
		address = self.binary.pointer
		self.binary.write(0x00)										# branch offset
		return address
	#
	#		Complete a branch
	#
	def completeBranch(self,address,target):
		relative = target - (address + 1)
		self.binary.writeByte(address,relative & 0xFF)
	#
	#		Generate load/save vars at various levels.
	#
	def variableAccess(self,isSave,address):
		if isSave:
			self.binary.write(0x22)									# LD (address),Hl
			self.binary.write2(address)
		else:
			self.binary.write(0xEB)									# EX DE,HL
			self.binary.write(0x2A)									# LD HL,(address)
			self.binary.write2(address)
	#
	#		Generate call or macro code
	#
	def generateWordCode(self,address,wordType,name):
		if wordType == "macro":										# if macro
			count = self.binary.readByte(address+1)					# number of bytes to generate
			if count == 0 or count > 8:
				raise CompilerException("Bad macro ? Bad count "+name)
			for i in range(0,count):								# copy it out
				self.binary.write(self.binary.readByte(address+i+5))
		elif wordType == "word":
			self.binary.write(0xCD) 								# Z80 CALL
			self.binary.write2(address)
		else:
			assert False,"Bad word type "+wordType
