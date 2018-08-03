rm test.sna
sh build.sh
fuse --debugger-command "br 0x5B00" __test.sna 2>/dev/null