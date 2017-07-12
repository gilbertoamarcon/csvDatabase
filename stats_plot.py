#!/usr/bin/python
import os
import statistics as stat
from CsvDatabase import *
from StatsFilter import *
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Parameters
C				= ['b','g','r','y','c','m']
BAR_FILL		= 0.75
FONT_SIZE		= 8
FONT_FAMILY		= 'serif'
VBAR			= True
DOMAIN			= 'blocks_world'

# Labels
lmetrics	= ['Makespan (s)', 'Actions', 'Proc. Time (s)', 'Memory (GB)']
lplanners	= ['tfd/downward', 'colin2']
ltools		= ['CFP', 'CoalitionAssistance']

def generate_plot(metrics,ltools):
	plt.figure(1)
	matplotlib.rcParams.update({'font.size': FONT_SIZE})
	matplotlib.rcParams.update({'font.family': FONT_FAMILY})
	if VBAR:
		subplot_pfix = 100 + 10*len(metrics)
	else:
		subplot_pfix = 10 + 100*len(metrics)
	numbars = len(ltools)
	bar_origin = ((1-BAR_FILL)/2)*np.ones(numbars) + np.asarray(range(numbars))

	# For each metric
	for m, metric in enumerate(metrics):
		planners = metrics[metric]
		lplanners = [p for p in planners]
		bar_width = BAR_FILL/len(lplanners)

		plt.subplot(subplot_pfix+m)
		plt.title(metric) 

		# For each planner
		for p, planner in enumerate(planners):
			tools = planners[planner]

			shift_pos = bar_origin+bar_width*p
			if VBAR:
				plt.bar(shift_pos, tools['mean'], bar_width, color=C[p], yerr=tools['error'], ecolor='k')
			else:
				plt.barh(shift_pos, tools['mean'], bar_width, color=C[p], xerr=tools['error'], ecolor='k')
		
		# Legend and ticks
		plt.legend(lplanners)
		if VBAR:
			plt.xticks(bar_origin+BAR_FILL/2, ltools)
			plt.xlim([0, numbars])
		else:
			plt.yticks(bar_origin+BAR_FILL/2, ltools)
			plt.ylim([0, numbars]) 

	# plt.savefig(title+".svg")
	plt.show()

def get_stats(sample):
	mean = stat.mean(sample)
	error = stat.stdev(sample)/len(sample)**0.5
	return mean, error

# Gathering data
os.system("./gather_data.sh")

# Filtering CSV file
StatsFilter.filter("stats.csv","stats_filtered.csv")

# Creating database
db = CsvDatabase('stats_filtered.csv')

# For each metric
metrics = {}
for metric in lmetrics:

	# For each planner
	planners = {}
	for planner in lplanners:
		tools = {}
		tools['mean'] = []
		tools['error'] = []
		for tool in ltools:
			query = db.query([('Domain',DOMAIN),('Planner',planner),('Tool',tool),('Status','0')])
			select = db.select(metric, query, as_float=True)
			mean, error = get_stats(select)
			print "%6.1f [%6.1f]" % (mean, error)
			print "%6.1f [%6.1f]" % (mean, error)
			tools['mean'].append(mean)
			tools['error'].append(error)
		planners[planner] = tools
	metrics[metric] = planners

generate_plot(metrics,ltools)

