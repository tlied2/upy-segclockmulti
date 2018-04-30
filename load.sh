#!/bin/sh

PORT="/dev/ttyUSB0"

FILES="\
config.json \
main.py \
mysegdisplay.py \
mytz.py \
upy-mylib/mywifi.py \
"

for FILE in $FILES; do
echo ampy -p $PORT put $FILE ;
ampy -p $PORT put $FILE ;
done
