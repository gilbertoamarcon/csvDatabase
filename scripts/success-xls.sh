#!/bin/bash

# ./scripts/success-xls.sh

ratios=(0.25 0.50 0.75)
# ratios=(0.25)

for i in blocks_world,tfddownward blocks_world,colin2 first_response,colin2; do IFS=","; set -- $i;
# for i in blocks_world,tfddownward; do IFS=","; set -- $i;
	domain=$1
	planner=$2
	for fr in ${ratios[@]}; do python src/success.py -p $planner -d $domain -f $fr; done
done