# ****************************************************************************************
# ****************************************************************************************
#
#		Name:		binary.py
#		Purpose:	M13 Binary Object
#		Date:		1st August 2018
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ****************************************************************************************
# ****************************************************************************************

from dictionary import *

# ****************************************************************************************
#											Binary object
# ****************************************************************************************

class M13Binary(object):
	def __init__(self,source,dictionary):
		self.loadAddress = 0x5B00 									# binary starts here
		self.source = source
		self.memory = [ 0x00 ] * 0x10000							# memory representation
		binary = [x for x in open(source,"rb").read(-1)]			# read binary and copy into memory
		for i in range(0,len(binary)):
			self.memory[self.loadAddress+i] = binary[i]
		self.lastAddress = self.loadAddress + len(binary)			# highest address accessed
		self.sysInfo = dictionary.find("sys.info").getAddress()		# where sys.info is.
		self.pointer = self.readWord(self.sysInfo + 8) 				# next free program pointer
		self.echo = True
		if self.echo:
			self.listing = open("m13.listing","w")
	#
	#		Read/Write methods
	#
	def readByte(self,address):
		return self.memory[address]
	def readWord(self,address):
		return self.readByte(address)+self.readByte(address+1) * 256
	def writeByte(self,address,data):
		if self.echo:
			self.listing.write("{0:04x} : {1:02x}\n".format(address,data))
		self.memory[address] = data
		self.lastAddress = max(self.lastAddress,address)
	def writeWord(self,address,data):
		self.writeByte(address,data & 0xFF)
		self.writeByte(address+1,data >> 8)
	def write(self,data):
		self.writeByte(self.pointer,data)
		self.pointer += 1
	def write2(self,data):
		self.writeWord(self.pointer,data)
		self.pointer += 2
	#
	#		Update the pointers in cold start/mark+empty and write binary out.
	#
	def save(self,fileName,dictionary):
		self.writeWord(self.sysInfo+8,self.lastAddress) 			# update next free code address
		main = dictionary.find("main")								# look for main
		if main is not None:										# if main found update main address
			self.writeWord(self.sysInfo+24,main.getAddress())
		self.echo = False
		self.listing.close()
		self.listing = None
		for i in range(0,6):										# copy current to cold start/mark
			self.writeByte(self.sysInfo+12+i,self.readByte(self.sysInfo+6+i))
			self.writeByte(self.sysInfo+18+i,self.readByte(self.sysInfo+6+i))
		h = open(fileName,"wb")										# write .bin file
		h.write(bytes(self.memory[self.loadAddress:self.lastAddress]))
		h.close()		

if __name__ == '__main__':
	dict = Dictionary("core.dictionary")
	bin = M13Binary("core.m13",dict)
	bin.save("test.m13",dict)
	print("{0:04x}".format(bin.sysInfo))

