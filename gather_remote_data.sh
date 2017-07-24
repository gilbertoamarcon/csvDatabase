#!/bin/bash
printf "" > csv/stats.csv
ssh ovunc 'cat ~/Documents/stats.csv' >> csv/stats.csv
ssh deskhp 'cat ~/Documents/stats.csv' >> csv/stats.csv
