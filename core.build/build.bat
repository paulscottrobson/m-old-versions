@ECHO OFF
REM
REM		delete files that are created by running this batch file.
REM
del /Q asm\*.asm 
del /Q system.bin 
del /Q system.bin.vice
del /Q core.m13 
del /Q core.dictionary
REM 
REM		Builds the two assembler files "macro.asm" and "word.asm" from the individual
REM 		word and macro definition
REM
python scanner.py
REM
REM		Creates the system machine code file 'system.bin' which is the core assembler 
REM		and the label listing file system.bin.vice
REM
..\bin\snasm -vice -next system.asm system.bin
copy system.bin core.m13 
REM
REM		Convert system.bin.vice to a dictionary listing
REM 
python createdictionary.py
copy core.m13 ..\compiler
copy core.dictionary ..\compiler


