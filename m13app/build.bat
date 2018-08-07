@echo off
del /Q core.m13
del /Q core.dictionary
del /Q build\m13app.m13
del /Q build\__m13app.sna
pushd ..\core.build
call build.bat
popd
if exist ..\compiler\core.m13 python ..\compiler\m13c.py
if exist build\m13app.m13 python ..\compiler\importdict.py
if exist build\m13app.m13 ..\bin\snasm -zxnext -brk -cur build\__m13app.asm