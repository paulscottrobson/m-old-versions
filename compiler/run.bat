@echo off
call build.bat
if exist build\__test.sna ..\bin\cspect.exe -zxnext -brk build\__test.sna