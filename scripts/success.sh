#!/bin/bash

python src/success.py -p tfddownward	-d blocks_world
python src/success.py -p colin2			-d blocks_world
python src/success.py -p colin2			-d first_response
python src/svg_stack.py --direction=v plots/prob_blocks_world_tfddownward.svg plots/prob_blocks_world_colin2.svg plots/prob_first_response_colin2.svg > plots/problems.svg
inkscape plots/problems.svg -E plots/problems.eps --export-ignore-filters
