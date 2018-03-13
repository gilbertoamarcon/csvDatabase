#!/bin/bash
grid=k
fr=0.50
out_fname=problem$fr
python src/success.py -p tfddownward	-d blocks_world		-f $fr -g $grid
python src/success.py -p colin2			-d blocks_world		-f $fr -g $grid
python src/success.py -p colin2			-d first_response	-f $fr -g $grid
python src/svg_stack.py --direction=v plots/prob_blocks_world_tfddownward.svg plots/prob_blocks_world_colin2.svg plots/prob_first_response_colin2.svg > plots/$out_fname.svg
inkscape plots/$out_fname.svg -E plots/$out_fname.eps --export-ignore-filters
fr=0.25
out_fname=problem$fr
python src/success.py -p tfddownward	-d blocks_world		-f $fr -g $grid
python src/success.py -p colin2			-d blocks_world		-f $fr -g $grid
python src/success.py -p colin2			-d first_response	-f $fr -g $grid
python src/svg_stack.py --direction=v plots/prob_blocks_world_tfddownward.svg plots/prob_blocks_world_colin2.svg plots/prob_first_response_colin2.svg > plots/$out_fname.svg
inkscape plots/$out_fname.svg -E plots/$out_fname.eps --export-ignore-filters
