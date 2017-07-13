#!/usr/bin/python
import os
import sys
import statistics as stat
from CsvDatabase import *
from StatsFilter import *
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Parameters
C				= ['b','g','r','y','c','m']
BAR_FILL		= 0.60
FONT_SIZE		= 8
FONT_FAMILY		= 'serif'
VBAR			= False
SHOW_PLOT		= False
DOMAIN			= 'blocks_world'
PSPACING		= 21
CSPACING		= 1
PLOT_NAME		= "plot"
FIG_SIZE		= (4, 5)
LEGEND			= False

# Labels
lmetrics	= ['Plan Length - Makespan (s)', 'Number of Actions', 'Processing Time (s)', 'Memory Usage (GB)', 'Success Rate (%)']
lplanners	= ['tfd/downward', 'colin2']
ltools		= ['CFP', 'CoalitionAssistance']

# Neat Names
NPLANNERS = {'tfd/downward': 'TFD', 'colin2': 'COLIN2'}

def generate_table(metrics, ltools):
	sys.stdout.write("% *s" % (PSPACING,"Planner"))
	for t in ltools:
		sys.stdout.write("% *s" % (PSPACING,t))
	print ""
	for metric in metrics:
		print "%s: " % metric
		planners = metrics[metric]
		for planner in planners:
			tools = planners[planner]
			sys.stdout.write("% *s" % (PSPACING,planner))
			for tool in tools['mean']:
				sys.stdout.write(" %*.*f" % (PSPACING-1,CSPACING,tool))
			print ""

def generate_plot(metrics,ltools):
	plt.figure(figsize=FIG_SIZE)
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
		lplanners = []
		for p in planners:
			lplanners.append(NPLANNERS[p])
		bar_width = BAR_FILL/len(lplanners)

		ax = plt.subplot(subplot_pfix+m+1)
		ax.xaxis.grid(True, which='major')
		ax.set_axisbelow(True)
		plt.title(metric) 

		# For each planner
		for p, planner in enumerate(planners):
			tools = planners[planner]

			shift_pos = bar_origin+bar_width*p
			if VBAR:
				plt.bar(shift_pos, tools['mean'], bar_width, color=C[p], yerr=tools['error'], ecolor='k')
			else:
				plt.barh(shift_pos, tools['mean'], bar_width, color=C[p], xerr=tools['error'], ecolor='k')

		if VBAR:
			plt.xticks(bar_origin+BAR_FILL/2, ltools)
			plt.xlim([0, numbars])
		else:
			plt.yticks(bar_origin+BAR_FILL/2, ltools)
			plt.ylim([0, numbars]) 


	# Legend and ticks
	plt.tight_layout()
	plt.legend(lplanners, loc='lower center', bbox_to_anchor=(0.5,-1.0), ncol=2)
	plt.savefig(PLOT_NAME+".svg", bbox_inches='tight')
	if SHOW_PLOT:
		plt.show()

def get_stats(sample):
	mean = stat.mean(sample)
	error = stat.stdev(sample)/len(sample)**0.5
	return mean, error

# Gathering data
os.system("./gather_data.sh")

# Filtering CSV file
StatsFilter.filter("csv/stats.csv","csv/stats_filtered.csv")

# Creating database
db = CsvDatabase('csv/stats_filtered.csv')

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
			if metric == lmetrics[-1:][0]:
				tools['mean'].append(len(query))
				tools['error'].append(0)
			else:
				select = db.select(metric, query, as_float=True)
				mean, error = get_stats(select)
				tools['mean'].append(mean)
				tools['error'].append(error)
		planners[planner] = tools
	metrics[metric] = planners

generate_table(metrics,ltools)
generate_plot(metrics,ltools)

