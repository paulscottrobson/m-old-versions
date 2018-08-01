# ****************************************************************************************
# ****************************************************************************************
#
#		Name:		dictionary.py
#		Purpose:	Dictionary Object
#		Date:		1st August 2018
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ****************************************************************************************
# ****************************************************************************************

# ****************************************************************************************
#								Dictionary Item Classes
# ****************************************************************************************

class BaseDictionaryItem(object):
	def __init__(self,name,address):
		self.name = name.strip().lower()
		self.address = address
		self.private = False
	#
	def getName(self):
		return self.name
	def getAddress(self):
		return self.address
	def isPrivate(self):
		return self.private
	def toString(self):
		return "{0:04x}::{1}::{2}".format(self.getAddress(),self.getType(),self.getName())
	def makePrivate(self):
		self.private = True

class WordDictionaryItem(BaseDictionaryItem):
	def getType(self):
		return "word"

class ImmediateWordDictionaryItem(BaseDictionaryItem):
	def getType(self):
		return "immediate"

class MacroDictionaryItem(BaseDictionaryItem):
	def getType(self):
		return "macro"

class VariableDictionaryItem(BaseDictionaryItem):
	def getType(self):
		return "variable"
	def isPrivate(self):
		return True

# ****************************************************************************************
#									Dictionary Class
# ****************************************************************************************

class Dictionary(object):
	def __init__(self,source):
		self.words = {}												# word storage
		self.source = source
		for l in [x.strip().lower() for x in open(source).readlines()]:
			if l != "":
				l = l.split("::")									# read in dictionary entry and add it
				self.add(l[2],l[1],int(l[0],16))
	#
	#		Add an entry
	#
	def add(self,word,type,address):
		self.lastEntry = None
		if type == "word":
			self.lastEntry = WordDictionaryItem(word,address)
		if type == "macro":
			self.lastEntry = MacroDictionaryItem(word,address)
		if type == "variable":
			self.lastEntry = VariableDictionaryItem(word,address)
		if type == "immediate":
			self.lastEntry = ImmediateWordDictionaryItem(word,address)
		assert self.lastEntry is not None,"Cannot create DictionaryItem object"		
		self.words[word] = self.lastEntry
		return self.lastEntry
	#
	#		Find an entry
	#
	def find(self,word):
		word = word.lower()
		return self.words[word] if word in self.words else None
	#
	#		Get all entries in address order
	#
	def getAllWordNames(self):
		wordList = [x for x in self.words.keys()]					# keys
		wordList.sort(key = lambda x:self.words[x].getAddress())	# sort by address
		return wordList

	#
	#		Write dictionary file out.
	#
	def writeDictionary(self,target):
		assert self.source != target,"Cannot write back to original"
		wordList = self.getAllWordNames()
		h = open(target,"w")
		for w in wordList:											# scan through
			if not self.words[w].isPrivate():						# don't render private
				h.write(self.words[w].toString()+"\n")
		h.close()
	#
	#		Make last private/immediate
	#
	def makeLastPrivate(self):
		self.lastEntry.makePrivate()
	def makeLastImmediate(self):
		assert isinstance(self.lastEntry,WordDictionaryItem),"Cannot make non words immediate"
		self.lastEntry = ImmediateWordDictionaryItem(self.lastEntry.getName(),self.lastEntry.getAddress())
		self.words[self.lastEntry.getName()] = self.lastEntry

if __name__ == '__main__':
	dict = Dictionary("core.dictionary")
	print(dict.find("COPY").toString())
	print(dict.find("POP.BB").toString())	
	v = dict.add("var","variable",0xC001)
	i = dict.add("imm","word",0xD002)
	print(dict.find("VAR").toString())
	print(dict.find("imm").toString())

	dict.writeDictionary("test.dictionary")