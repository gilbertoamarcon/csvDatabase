#!/bin/bash

rm plots/*.svg
python src/main.py -p tfddownward	-d blocks_world
python src/main.py -p colin2		-d blocks_world
python src/main.py -p colin2		-d first_response
python src/svg_stack.py --direction=v $(ls plots/*.svg) > plots/boxes.svg
inkscape plots/boxes.svg -E plots/boxes.eps --export-ignore-filters