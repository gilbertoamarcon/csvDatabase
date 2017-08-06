#!/bin/bash
printf "" > csv/stats.csv
results_dir=${HOME}/dev/test-results
dirs=$(ls $results_dir)
for d in $dirs; do
	if [ -d $results_dir/$d ]; then
		cat $results_dir/$d/stats.csv >> csv/stats.csv
	fi
done
cat csv/stats.csv | sed 's/ -s\s*\/home\/gil\/Documents\/stats.csv//g' | sed 's/\/home\/\w*\/Documents\/prob //g' | sed 's/-sm //g' | sed 's/-so //g' > csv/stats_.csv
cp csv/stats_.csv csv/stats.csv
rm csv/stats_.csv
