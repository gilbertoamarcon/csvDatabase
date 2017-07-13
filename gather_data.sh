#!/bin/bash
tabs -4
printf "" > csv/stats.csv
ssh ovunc 'cat ~/Documents/stats.csv' >> csv/stats.csv
ssh deskhp 'cat ~/Documents/stats.csv' >> csv/stats.csv
