#!/bin/bash
printf "" > stats.csv
ssh ovunc 'cat ~/Documents/stats.csv' >> stats.csv
ssh deskhp 'cat ~/Documents/stats.csv' >> stats.csv
