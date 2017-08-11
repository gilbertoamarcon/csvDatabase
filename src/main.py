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
from scipy import stats

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
		(0.000, 0.447, 0.741), # Blue
		(0.850, 0.325, 0.098), # Tomato
		(0.929, 0.694, 0.125), # Orange
		(0.929, 0.894, 0.325), # Yellow
		(0.000, 0.447, 0.741), # Blue
		(0.850, 0.325, 0.098), # Tomato
		(0.929, 0.694, 0.125), # Orange
		(0.929, 0.894, 0.325), # Yellow
		(0.950, 0.525, 0.298), # Salmon
		(0.301, 0.745, 0.933), # Light Blue
	]

BAR_FILL		= 0.60
FONT_SIZE		= 8
FONT_FAMILY		= 'serif'
SHOW_PLOT		= False
# DOMAIN			= 'blocks_world'
DOMAIN			= 'first_response'
COL_PAD			= 5
CSPACING		= 1
FIG_SIZE		= (4, 7)
LEGEND			= False

# File names
GATHER_DATA_SCRIPT	= "scripts/gather_data.sh"
RAW_STATS			= "csv/stats.csv"
FILTERED_STATS		= "csv/stats_filtered.csv"
STATS_TABLE			= "csv/stats_table.csv"
P_TABLE				= "csv/p_table.csv"
MAIN_PLOT_NAME		= "main_plot.pdf"
HIST_PLOT_NAME		= "hist_plot.pdf"


# Labels

header		= ['Domain','Problem','CFA','Planner','Tool','Makespan (s)','Number of Actions','Processing Time (s)','Memory Usage (GB)','Planning Results (%)']
lmetrics	= header[-5:]
lplanners	= ['colin2']
# lplanners	= ['tfddownward', 'colin2']
ltools		= ['CFP', 'Object', 'ObjectTime', 'Makespan', 'IdleTime']
# ltools		= ['CFP', 'Object', 'ObjectTime', 'ActionObject', 'ActionObjectTime', 'Makespan', 'IdleTime', 'CoalitionAssistance', 'CoalitionSimilarity', 'PA']

# Neat Names
NPLANNERS = {'tfddownward': 'TFD', 'colin2': 'COLIN2'}

def p_test(metrics, ltools):
	p_test_results = {}
	for m, metric in enumerate(metrics):
		if m < len(metrics)-1:
			# p_test_results[metric] = {}
			planners = metrics[metric]
			for p, planner in enumerate(planners):
				for i, t1 in enumerate(planners[planner]['sample']):
					for j, t2 in enumerate(planners[planner]['sample']):
						if j > i:
							if (ltools[i], ltools[j]) not in p_test_results:
								p_test_results[(ltools[i], ltools[j])] = {}
							p_test_results[(ltools[i], ltools[j])][metric] = stats.kruskal(t1,t2)
	return p_test_results

def p_test_table(p_test_results):
	ret_var = ""
	for p in p_test_results:
		ret_var += 'Pair,'
		for m in p_test_results[p]:
			ret_var += "%sH(p)," % m
		ret_var += "\n"
		break
	for p in p_test_results:
		ret_var += '\"%s-%s\",' % p
		for m in p_test_results[p]:
			ret_var += "%0.4f(%0.4f)," % p_test_results[p][m]
		ret_var += "\n"
	return ret_var

def generate_main_table(metrics, ltools, separator=None):

	# Assembling stats_table
	stats_table = []
	trow = []

	# Header
	for h in ["Metric", "Planner"] + ltools:
		trow.append(h)
	stats_table.append(trow)

	# Body
	for metric in metrics:
		for planner in metrics[metric]:
			if metric == "Planning Results (%)":
				succ = ['Success (%)', 'Nonexecutable (%)', 'Time Fail (%)', 'Memory Fail (%)']
				for s in succ:
					trow = []
					for r in ["\"%s\""%s, NPLANNERS[planner]] + ["%.*f"%(CSPACING,v) for v in metrics[metric][planner][s]]:
						trow.append(r)
					stats_table.append(trow)
			else:
				trow = []
				num_elements = len(metrics[metric][planner]['mean'])
				content = []
				for i in range(num_elements):
					content.append("%.*f(%.*f)"%(CSPACING,metrics[metric][planner]['mean'][i],CSPACING,metrics[metric][planner]['error'][i]))
				for r in ["\"%s\""%metric, NPLANNERS[planner]] + content:
					trow.append(r)
				stats_table.append(trow)
	
	# Getting column widths
	if separator is None:
		col_widths = OrderedDict()
		for j in range(len(stats_table[0])):
			col_width = 0
			for e in stats_table:
				col_width = max(len(e[j]),col_width)
			col_widths[j] = col_width+COL_PAD

	# Lists to string
	ret_var = ""
	for i in range(len(stats_table)):
		for j in range(len(stats_table[0])):
			if separator is None:
				ret_var += "% *s" % (col_widths[j],stats_table[i][j])
			else:
				ret_var += "%s%s" % (stats_table[i][j],separator)
		ret_var += "\n"
	return ret_var

def generate_main_plot(metrics,ltools):
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
					if len(lplanners)> 1:
						prefix = lp+" "
					else:
						prefix = ""
					label_succ.append(prefix+"Mem Fail")
					label_succ.append(prefix+"Time Fail")
					label_succ.append(prefix+"Nonexecutable")
					label_succ.append(prefix+"Success")
				success = np.array(tools['Success (%)'])
				nonex = np.array(tools['Nonexecutable (%)'])
				time = np.array(tools['Time Fail (%)'])
				mem = np.array(tools['Memory Fail (%)'])
				plt.barh(shift_pos, success+nonex+time+mem, bar_width, color=S[4*p+3])
				plt.barh(shift_pos, success+nonex+time, bar_width, color=S[4*p+2])
				plt.barh(shift_pos, success+nonex, bar_width, color=S[4*p+1])
				plt.barh(shift_pos, success, bar_width, color=S[4*p+0])
				plt.legend(label_succ, loc='lower center', bbox_to_anchor=(0.5,-2.0), ncol=2)

		plt.xlabel(metric)
		plt.yticks(bar_origin+BAR_FILL/2, ltools)
		plt.ylim([0, numbars]) 

		if m == 0:
			plt.legend(lplanners, loc='lower center', bbox_to_anchor=(0.5,1.0), ncol=2)

	# Legend and ticks
	plt.tight_layout()
	plt.savefig(MAIN_PLOT_NAME, bbox_inches='tight')
	if SHOW_PLOT:
		plt.show()

def generate_hist_plots(metrics,ltools):
	plt.figure(figsize=FIG_SIZE)
	matplotlib.rcParams.update({'font.size': FONT_SIZE})
	matplotlib.rcParams.update({'font.family': FONT_FAMILY})
	subplot_pfix = 10 + 100*len(metrics)

	# For each metric
	for m, metric in enumerate(metrics):
		if m < len(metrics)-1:

			planners = metrics[metric]
			lplanners = []
			for p in planners:
				lplanners.append(NPLANNERS[p])

			ax = plt.subplot(subplot_pfix+m+1)
			ax.yaxis.grid(True, which='major')
			ax.set_axisbelow(True)

			# For each planner
			for p, planner in enumerate(planners):
				for i, t in enumerate(planners[planner]['hist']):
					x_array = np.asarray(range(len(t[0])))
					plt.bar(x_array, t[0], 1.0, color=C[i], alpha=0.5)
					for lx, l in enumerate(t[1]):
						t[1][lx] = "%.1f" % float(l)

			plt.xlabel(metric)
			plt.xticks(x_array, t[1])
			plt.xlim([0, len(t[0])]) 

		if m == 0:
			plt.legend(ltools, loc='lower center', bbox_to_anchor=(0.5,1.0), ncol=2)

	# Legend and ticks
	plt.tight_layout()
	plt.savefig(HIST_PLOT_NAME, bbox_inches='tight')
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
		tools['mean']				= []
		tools['Success (%)']		= []
		tools['Nonexecutable (%)']	= []
		tools['Time Fail (%)']		= []
		tools['Memory Fail (%)']	= []
		tools['error']				= []
		tools['sample']				= []
		tools['hist']				= []
		limits_query = db.query([('Domain',DOMAIN),('Planner',planner),('Planning Results (%)','0')])
		for tool in ltools:
			# query = db.query([('Domain',DOMAIN),('Planner',planner),('Tool',tool)])
			query = db.query([('Domain',DOMAIN),('Planner',planner),('Tool',tool),('Planning Results (%)','0')])
			if metric == lmetrics[-1:][0]:
				query_all = db.query([('Domain',DOMAIN),('Planner',planner),('Tool',tool)])
				success = db.select('Planning Results (%)', query_all, as_integer=True)
				time = db.select('Processing Time (s)', query_all, as_integer=True)
				n = len(query_all)
				nonex_count = 0
				time_count = 0
				mem_count = 0
				for i in range(0,n):
					if success[i] == 1:
						nonex_count += 1
					if success[i] == 124:
						time_count += 1
					if success[i] == 134:
						mem_count += 1
				tools['Success (%)'].append(100.0*len(query)/n)
				tools['Nonexecutable (%)'].append(100.0*nonex_count/n)
				tools['Time Fail (%)'].append(100.0*time_count/n)
				tools['Memory Fail (%)'].append(100.0*mem_count/n)
				tools['mean'].append(0)
				tools['error'].append(0)
			else:
				limits = db.select(metric, limits_query, as_float=True)
				select = db.select(metric, query, as_float=True)
				mean, error = get_stats(select)
				tools['mean'].append(mean)
				tools['error'].append(error)
				tools['sample'].append(select)
				tools['hist'].append(np.histogram(select, density=True, bins=8, range=(min(limits),max(limits))))
		planners[planner] = tools
	metrics[metric] = planners

p_test_results = p_test(metrics,ltools)

# Generating outputs
with open(STATS_TABLE, 'wb') as f:
	f.write(generate_main_table(metrics,ltools,","))
with open(P_TABLE, 'wb') as f:
	f.write(p_test_table(p_test_results))
generate_main_plot(metrics,ltools)
generate_hist_plots(metrics,ltools)

