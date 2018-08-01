#
#		Delete files that are created by running this batch file.
#
rm asm/*.asm system.bin system.lst core.m13 core.dictionary
# 
#		Builds the two assembler files "macro.asm" and "word.asm" from the individual
# 		word and macro definition
#
python scanner.py
#
#		Creates the system machine code file 'system.bin' which is the core assembler 
#		and the listing file system.lst
#
zasm -buw system.asm -l system.lst -o system.bin
cp system.bin core.m13 
#
#		Convert system.lst to a dictionary listing
# 
python createdictionary.py
cp core.m13 core.dictionary ../compiler


