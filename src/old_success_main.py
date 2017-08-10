#!/usr/bin/python
import os
import sys
import statistics as stat
from CsvDatabase import *
from StatsFilter import *
from collections import OrderedDict
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Parameters
C	= [
		(0.000, 0.447, 0.741),
		(0.850, 0.325, 0.098),
		(0.929, 0.694, 0.125),
		(0.494, 0.184, 0.556),
		(0.466, 0.674, 0.188),
		(0.301, 0.745, 0.933),
		(0.635, 0.078, 0.184),
	]
S	= [
		(0.929, 0.694, 0.125),
		(0.850, 0.325, 0.098),
		(0.000, 0.447, 0.741),
		(0.929, 0.894, 0.325),
		(0.950, 0.525, 0.298),
		(0.301, 0.745, 0.933),
	]
BAR_FILL		= 0.60
FONT_SIZE		= 8
FONT_FAMILY		= 'serif'
SHOW_PLOT		= False
DOMAIN			= 'blocks_world'
COL_PAD			= 5
CSPACING		= 1
FIG_SIZE		= (4, 12)
LEGEND			= False

# File names
GATHER_DATA_SCRIPT	= "./gather_data.sh"
RAW_STATS			= "csv/stats.csv"
FILTERED_STATS		= "csv/stats_filtered.csv"
TABLE_OUT			= "csv/table.csv"
PLOT_NAME			= "plot.pdf"


# Labels

header		= ['Domain','Problem','CFA','Planner','Tool','Makespan (s)','Number of Actions','Processing Time (s)','Memory Usage (GB)','Planning Results (%)']
lmetrics	= header[-5:]
lplanners	= ['colin2']
# lplanners	= ['tfd/downward', 'colin2']
ltools		= ['CFP', 'Object', 'ObjectTime']
# ltools		= ['CFP', 'CoalitionAssistance', 'CoalitionSimilarity', 'Object', 'ObjectTime', 'ActionObject', 'ActionObjectTime', 'Makespan', 'IdleTime', 'PA']

# Neat Names
NPLANNERS = {'tfd/downward': 'TFD', 'colin2': 'COLIN2'}

def generate_table(metrics, ltools, separator=None):

	# Assembling table
	table = []
	trow = []

	# Header
	for h in ["Metric", "Planner"] + ltools:
		trow.append(h)
	table.append(trow)

	# Body
	for metric in metrics:
		for planner in metrics[metric]:
			trow = []
			for r in ["\"%s\""%metric, NPLANNERS[planner]] + ["%.*f"%(CSPACING,v) for v in metrics[metric][planner]['mean']]:
				trow.append(r)
			table.append(trow)
	
	# Getting column widths
	if separator is None:
		col_widths = OrderedDict()
		for j in range(len(table[0])):
			col_width = 0
			for e in table:
				col_width = max(len(e[j]),col_width)
			col_widths[j] = col_width+COL_PAD

	# Lists to string
	ret_var = ""
	for i in range(len(table)):
		for j in range(len(table[0])):
			if separator is None:
				ret_var += "% *s" % (col_widths[j],table[i][j])
			else:
				ret_var += "%s%s" % (table[i][j],separator)
		ret_var += "\n"
	return ret_var

def generate_plot(metrics,ltools):
	plt.figure(figsize=FIG_SIZE)
	matplotlib.rcParams.update({'font.size': FONT_SIZE})
	matplotlib.rcParams.update({'font.family': FONT_FAMILY})
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
		# plt.title(metric) 

		# For each planner
		for p, planner in enumerate(planners):
			tools = planners[planner]

			shift_pos = bar_origin+bar_width*p
			if m < len(metrics)-1:
				plt.barh(shift_pos, tools['mean'], bar_width, color=C[p], xerr=tools['error'], ecolor='k')
			else:
				label_succ = []
				for lp in lplanners:
					label_succ.append(lp+" "+"Time Fail")
					label_succ.append(lp+" "+"Mem Fail")
					label_succ.append(lp+" "+"Success")
				success = np.array(tools['success'])
				mem = np.array(tools['mem'])
				time = np.array(tools['time'])
				plt.barh(shift_pos, success+mem+time, bar_width, color=S[3*p+0])
				plt.barh(shift_pos, success+mem, bar_width, color=S[3*p+1])
				plt.barh(shift_pos, success, bar_width, color=S[3*p+2])
				plt.legend(label_succ, loc='lower center', bbox_to_anchor=(0.5,-0.7), ncol=2)

		plt.xlabel(metric)
		plt.yticks(bar_origin+BAR_FILL/2, ltools)
		plt.ylim([0, numbars]) 

		if m == 0:
			plt.legend(lplanners, loc='lower center', bbox_to_anchor=(0.5,1.0), ncol=2)


	# Legend and ticks
	plt.tight_layout()
	plt.savefig(PLOT_NAME, bbox_inches='tight')
	if SHOW_PLOT:
		plt.show()

def get_stats(sample):
	mean = stat.mean(sample)
	error = stat.stdev(sample)/len(sample)**0.5
	return mean, error

# Gathering data
os.system(GATHER_DATA_SCRIPT)

# Filtering CSV file
StatsFilter.filter(RAW_STATS,FILTERED_STATS,header)

# Creating database
db = CsvDatabase(FILTERED_STATS)

# For each metric
metrics = OrderedDict()
for metric in lmetrics:

	# For each planner
	planners = OrderedDict()
	for planner in lplanners:
		tools = OrderedDict()
		tools['mean'] = []
		tools['success'] = []
		tools['mem'] = []
		tools['time'] = []
		tools['error'] = []
		for tool in ltools:
			# query = db.query([('Domain',DOMAIN),('Planner',planner),('Tool',tool)])
			query = db.query([('Domain',DOMAIN),('Planner',planner),('Tool',tool),('Planning Results (%)','0')])
			if metric == lmetrics[-1:][0]:
				query_all = db.query([('Domain',DOMAIN),('Planner',planner),('Tool',tool)])
				success = db.select('Planning Results (%)', query_all, as_integer=True)
				time = db.select('Processing Time (s)', query_all, as_integer=True)
				n = len(query_all)
				time_count = 0
				mem_count = 0
				for i in range(0,n):
					if success[i]!= 0:
						if time[i] < 3600:
							mem_count += 1
						else:
							time_count += 1
				tools['success'].append(100.0*len(query)/n)
				tools['mem'].append(100.0*mem_count/n)
				tools['time'].append(100.0*time_count/n)
				tools['mean'].append(0)
				tools['error'].append(0)
			else:
				select = db.select(metric, query, as_float=True)
				mean, error = get_stats(select)
				tools['mean'].append(mean)
				tools['error'].append(error)
		planners[planner] = tools
	metrics[metric] = planners


# Generating outputs
with open(TABLE_OUT, 'wb') as f:
	f.write(generate_table(metrics,ltools,","))
print generate_table(metrics,ltools)
generate_plot(metrics,ltools)

