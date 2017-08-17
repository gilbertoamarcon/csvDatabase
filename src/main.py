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
		(0.929, 0.694, 0.125), # Orange
		(0.929, 0.894, 0.325), # Yellow
		(0.850, 0.325, 0.098), # Tomato

		(0.000, 0.000, 0.750), # Blue
		(1.000, 0.500, 0.000), # Orange
		(1.000, 1.000, 0.000), # Yellow
		(1.000, 0.000, 0.000), # Tomato
	]

BAR_FILL		= 0.60
FONT_SIZE		= 8
FONT_FAMILY		= 'serif'
SHOW_PLOT		= False
DOMAIN			= 'blocks_world'
# DOMAIN			= 'first_response'
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
PLOT_FORMATS		= ['pdf', 'svg', 'eps']
STATS_PLOT_NAME		= "plots/stats_plot"
PDF_PLOT_NAME		= "plots/pdf_plot"


# Labels

header		= ['Domain','Problem','CFA','Planner','Tool','Makespan (%)','Number of Actions (%)','Processing Time (%)','Memory Usage (%)','Planning Results (%)']
# header		= ['Domain','Problem','CFA','Planner','Tool','Makespan (%)','Number of Actions (%)','Processing Time (%)','Memory Usage (%)','Planning Results (%)']
lmetrics	= header[-5:]
# lplanners	= ['colin2']
lplanners	= ['tfddownward', 'colin2']
# ltools		= ['CFP', 'Object', 'ObjectTime', 'CoalitionAssistance', 'CoalitionSimilarity']
ltools		= ['CFP', 'Object', 'ObjectTime', 'CoalitionAssistance', 'CoalitionSimilarity', 'PA']
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
			ret_var += "%s," % m
			ret_var += "%s," % m
		ret_var += "\n"
		break
	for p in p_test_results:
		ret_var += '\"%s-%s\",' % p
		for m in p_test_results[p]:
			ret_var += "%0.4f,%0.4f," % p_test_results[p][m]
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

def generate_stats_plots(metrics,ltools):
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
					label_succ.append(prefix+"Nonexecutable")
					label_succ.append(prefix+"Mem Fail")
					label_succ.append(prefix+"Time Fail")
					label_succ.append(prefix+"Success")
				success = np.array(tools['Success (%)'])
				time = np.array(tools['Time Fail (%)'])
				mem = np.array(tools['Memory Fail (%)'])
				nonex = np.array(tools['Nonexecutable (%)'])
				plt.barh(shift_pos, success+time+mem+nonex, bar_width, color=S[4*p+3])
				plt.barh(shift_pos, success+time+mem, bar_width, color=S[4*p+2])
				plt.barh(shift_pos, success+time, bar_width, color=S[4*p+1])
				plt.barh(shift_pos, success, bar_width, color=S[4*p+0])
				plt.legend(label_succ, loc='lower center', bbox_to_anchor=(0.5,-1.5), ncol=2)
				plt.xlim([0, 100]) 

		plt.xlabel(metric)
		plt.yticks(bar_origin+BAR_FILL/2, ltools)
		plt.ylim([0, numbars]) 

		if m == 0:
			plt.legend(lplanners, loc='lower center', bbox_to_anchor=(0.5,1.0), ncol=2)

	# Legend and ticks
	plt.tight_layout()
	for f in PLOT_FORMATS:
		plt.savefig(STATS_PLOT_NAME+'.'+f, bbox_inches='tight')
	if SHOW_PLOT:
		plt.show()

def generate_pdf_plots(metrics,ltools):
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

			# Ranges
			max_range = 0
			for planner in planners:
				for i, tool in enumerate(planners[planner]['sample']):
					max_range = max(max(tool),max_range)

			# For each planner
			for p, planner in enumerate(planners):
				for i, t in enumerate(planners[planner]['kde']):
					t_range = np.linspace(0,1.5*max_range,100)
					plt.plot(t_range,t(t_range))

			plt.xlabel(metric)

		if m == 0:
			plt.legend(ltools, loc='lower center', bbox_to_anchor=(0.5,1.0), ncol=2)

	# Legend and ticks
	plt.tight_layout()
	for f in PLOT_FORMATS:
		plt.savefig(PDF_PLOT_NAME+'.'+f, bbox_inches='tight')
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

# Problems at which all tools succeeded
all_success_problems = []
for tool in ltools:
	all_success_problems.append(set(db.select('Problem', db.query([('Domain',DOMAIN),('Tool',tool),('Planning Results (%)','0')]))))
all_success_problems = sorted(list(set.intersection(*all_success_problems)))


# Stats on Problems Solved
solved_query = db.query([('Domain',DOMAIN), ('Planning Results (%)','0')])
solved_problems = set(db.select('Problem', solved_query))
problems_stats = {}
for s in solved_problems:
	problems_stats[s] = {}
	for metric in lmetrics:
		if metric != lmetrics[-1:][0]:
			problem_query = db.query([('Domain',DOMAIN), ('Planning Results (%)','0'), ('Problem',s)])
			problems_stats[s][metric] = db.select(metric, problem_query, as_float=True)

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
		tools['kde']				= []
		for tool in ltools:
			# query = db.query([('Domain',DOMAIN),('Planner',planner),('Tool',tool)])
			query = db.query([('Domain',DOMAIN),('Planner',planner),('Tool',tool),('Planning Results (%)','0')])
			if metric == lmetrics[-1:][0]:
				query_all = db.query([('Domain',DOMAIN),('Planner',planner),('Tool',tool)])
				success = db.select('Planning Results (%)', query_all, as_integer=True)
				time = db.select('Processing Time (%)', query_all, as_integer=True)
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
				normalized = []
				for p in db.select(['Problem', metric], query):
					normalized.append(100.00*float(p[1])/min(problems_stats[p[0]][metric]) - 100.00)
				mean, error = get_stats(normalized)
				tools['mean'].append(mean)
				tools['error'].append(error)
				tools['sample'].append(normalized)
				tools['kde'].append(stats.gaussian_kde(normalized))
		planners[planner] = tools
	metrics[metric] = planners

p_test_results = p_test(metrics,ltools)

# Generating outputs
with open(STATS_TABLE, 'wb') as f:
	f.write(generate_main_table(metrics,ltools,","))
with open(P_TABLE, 'wb') as f:
	f.write(p_test_table(p_test_results))
generate_stats_plots(metrics,ltools)
generate_pdf_plots(metrics,ltools)

