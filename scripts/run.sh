#!/bin/bash

# rm plots/*.svg
python src/main.py -p tfddownward	-d blocks_world
python src/main.py -p colin2		-d blocks_world
python src/main.py -p colin2		-d first_response
python src/svg_stack.py --direction=v plots/box_blocks_world_tfddownward.svg plots/box_blocks_world_colin2.svg plots/box_first_response_colin2.svg > plots/boxes.svg
inkscape plots/boxes.svg -E plots/boxes.eps --export-ignore-filters