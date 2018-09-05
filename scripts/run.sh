#!/bin/bash

# ./scripts/run.sh ${HOME}/over/18818311vzjzwvxvfcky/


dest=$1

python src/main.py -p tfddownward	-d blocks_world
python src/main.py -p colin2		-d blocks_world
python src/main.py -p colin2		-d first_response
if ! [ -z "$1" ]; then
	cp plots/*.eps $dest/fig/
	# cp tex/* $dest/tables/
fi