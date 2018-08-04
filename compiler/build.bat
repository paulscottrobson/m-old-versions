@echo off
pushd ..\core.build
call build.bat
popd
python ..\compiler\m13c.py
..\bin\snasm -zxnext -brk -cur build\__test.asm