cd ../core.build
sh build.bat
cd ../compiler
rm test.bin test.sna
python ../compiler/m13c.py
zasm -bu __test.asm