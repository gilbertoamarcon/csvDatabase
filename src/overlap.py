#!/usr/bin/python
import os
import csv
from collections import OrderedDict
from CsvDatabase import *
from StatsFilter import *

STATUS_FLAGS	= OrderedDict([('Success (%)',0), ('Nonexecutable (%)',1), ('Time Fail (%)',124), ('Memory Fail (%)',134)])
STATUS_SHORT	= OrderedDict([('Memory Fail (%)','Mem Fail'), ('Time Fail (%)','Time Fail'), ('Nonexecutable (%)','Nonexec'), ('Success (%)','Success')])
TOOLS_SHORT		= OrderedDict([('PA','PA'), ('CFP','CFP'), ('Object','O'), ('ObjectTime','OT'), ('Action','A'), ('ActionTime','AT'), ('ActionObject','AO'), ('ActionObjectTime','AOT'), ('CoalitionAssistance','CA'), ('CoalitionSimilarity','CS')])

DOMAIN			= 'first_response'
OVERLAP_PREF	= 'csv/overlap_'
# DOMAIN			= 'blocks_world'
# PLANNER			= 'tfddownward'
PLANNER			= 'colin2'

# File names
GATHER_DATA_SCRIPT	= "scripts/gather_data.sh"
RAW_STATS			= "csv/stats.csv"
FILTERED_STATS		= "csv/stats_filtered.csv"

# Labels
header		= ['Domain','Problem','CFA','Planner','Tool','Makespan (%)','Number of Actions (%)','Processing Time (%)','Memory Usage (%)','Planning Results (%)']

tools		= ['ActionObjectTime', 'ActionObject', 'ActionTime', 'Action', 'ObjectTime', 'Object', 'CoalitionAssistance', 'CoalitionSimilarity', 'CFP', 'PA']
FIG_SIZE	= (3.4, 15.0)
LABEL_OSET_RESULTS	= 0.5
LABEL_OSET_METRICS	= -0.6

tools_short = [TOOLS_SHORT[t] for t in tools]

# Gathering data
print 'Gathering data ...'
os.system(GATHER_DATA_SCRIPT)

# Filtering CSV file
print 'Filtering CSV file ...'
StatsFilter.filter(RAW_STATS,FILTERED_STATS,header)

# Creating database
print 'Creating database ...'
db = CsvDatabase(FILTERED_STATS)

for f in STATUS_FLAGS:
	trow = []
	trow.append(['']+list(reversed(tools_short)))
	for t1 in reversed(tools):
		tcol = []
		sel1 = db.select('Problem', db.query([('Domain',DOMAIN),('Planner',PLANNER),('Tool',t1),('Planning Results (%)',str(STATUS_FLAGS[f]))]))
		for t2 in reversed(tools):
			sel2 = db.select('Problem', db.query([('Domain',DOMAIN),('Planner',PLANNER),('Tool',t2),('Planning Results (%)',str(STATUS_FLAGS[f]))]))
			tcol.append(len(set(sel1) & set(sel2)))
		trow.append([TOOLS_SHORT[t1]]+tcol)
	with open(OVERLAP_PREF+STATUS_SHORT[f]+'.csv', "wb") as file:
		writer = csv.writer(file)
		writer.writerows(trow)
