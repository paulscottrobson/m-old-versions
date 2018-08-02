cd ../dictionary
sh build.bat
cd ../compiler
rm result.bin result.sna
python ../compiler/m13c.py
zasm -bu result.asm

# TODO: Figure out the key reading problem
	