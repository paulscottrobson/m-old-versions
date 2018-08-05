@echo off
call build.bat
if exist build\__m13app.sna ..\bin\cspect.exe -zxnext -brk build\__m13app.sna