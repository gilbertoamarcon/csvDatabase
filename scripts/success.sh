#!/bin/bash

# ./scripts/success.sh ${HOME}/over/14617918kcvdvjvrbpng/

dest=$1

grid=w
ratios=(0.25 0.50 0.75 1.00)

# for i in blocks_world,tfddownward blocks_world,colin2 first_response,colin2; do IFS=","; set -- $i;
for i in first_response,colin2; do IFS=","; set -- $i;
	domain=$1
	planner=$2
	name=plots/prob-$domain-$planner
	for fr in ${ratios[@]}; do python src/success.py -p $planner -d $domain -f $fr -g $grid; done
	for fr in ${ratios[@]}; do python src/remove_svg_frame.py -i $name-$fr.svg -o $name-$fr.svg; done
	echo $(for fr in ${ratios[@]}; do echo $name-$fr.svg; done) | xargs python src/svg_stack.py --direction=v > $name.svg
	python src/remove_svg_frame.py -i $name.svg -o $name.svg
	inkscape $name.svg -E $name.eps --export-ignore-filters
	if ! [ -z "$1" ]; then
		cp $name.eps $dest/fig/
	fi
done