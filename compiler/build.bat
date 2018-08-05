@echo off
del /Q core.m13
del /Q core.dictionary
del /Q build\test.m13
del /Q build\__test.sna
pushd ..\core.build
call build.bat
popd
if exist ..\compiler\core.m13 python ..\compiler\m13c.py
if exist build\test.m13 ..\bin\snasm -zxnext -brk -cur build\__test.asm