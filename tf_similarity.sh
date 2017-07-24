#!/bin/bash

domain="blocks_world"
probdir="data/blocks_world_colin2/results/"
tools=(CoalitionAssistance CoalitionSimilarity Object ObjectTime ActionObject ActionObjectTime Makespan IdleTime)

probs=$(echo P{01..10}C{01..10})

declare -A count
for a in $(seq 0 $((${#tools[@]}-1))); do
	for b in $(seq $((a+1)) $((${#tools[@]}-1))); do
		ta=${tools[$a]}
		tb=${tools[$b]}
		count["$ta $tb"]=0
	done
done

for p in $probs; do 
	for a in $(seq 0 $((${#tools[@]}-1))); do
		for b in $(seq $((a+1)) $((${#tools[@]}-1))); do
			ta=${tools[$a]}
			tb=${tools[$b]}
			outa=$probdir/tf_$ta/$p/stdout
			outb=$probdir/tf_$tb/$p/stdout
			bega=$(cat $outa | grep -n 'Coalitions Capabilities:' | cut -f1 -d: | tail -1)
			begb=$(cat $outb | grep -n 'Coalitions Capabilities:' | cut -f1 -d: | tail -1)
			enda=$(cat $outa | grep -n 'Coalition-Task Pairs:' | cut -f1 -d: | tail -1)
			endb=$(cat $outb | grep -n 'Coalition-Task Pairs:' | cut -f1 -d: | tail -1)
			ma=$(sed -n $((bega+1)),$((enda-2))p $outa | cut -f2 -d"	" | cut -f1 -d: )
			mb=$(sed -n $((begb+1)),$((endb-2))p $outb | cut -f2 -d"	" | cut -f1 -d: )
			if [ "$ma" == "$mb" ]; then
				count["$ta $tb"]=$((${count["$ta $tb"]}+1))
			fi
		done
	done
done

for a in $(seq 0 $((${#tools[@]}-1))); do
	for b in $(seq $((a+1)) $((${#tools[@]}-1))); do
		ta=${tools[$a]}
		tb=${tools[$b]}
		echo "$ta $tb: ${count["$ta $tb"]}"
	done
done