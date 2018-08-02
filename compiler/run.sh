rm result.sna
sh build.sh
fuse --debugger-command "br 0x4B00" result.sna 2>/dev/null