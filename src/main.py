#!/usr/bin/python
import os
import matplotlib
import matplotlib.pyplot as plt
import statistics as stat
import numpy as np
from tqdm import tqdm
from collections import OrderedDict
import matplotlib.gridspec as gridspec
from scipy import stats
from CsvDatabase import *
from StatsFilter import *

# Parameters
C	= [
		(0.000, 0.447, 0.741), # Blue
		(0.850, 0.325, 0.098), # Tomato
		(0.929, 0.694, 0.125), # Orange
		(0.929, 0.894, 0.325), # Yellow
	]

STATUS_FLAGS	= OrderedDict([('Success (%)',0), ('Nonexecutable (%)',1), ('Time Fail (%)',124), ('Memory Fail (%)',134)])
STATUS_SHORT	= OrderedDict([('Memory Fail (%)','Mem Fail'), ('Time Fail (%)','Time Fail'), ('Nonexecutable (%)','Nonexec'), ('Success (%)','Success')])
TOOLS_LONG		= OrderedDict([('PA','PA'), ('CFP','CFP'), ('Object','O'), ('ObjectTime','OT'), ('Action','A'), ('ActionTime','AT'), ('ActionObject','AO'), ('ActionObjectTime','AOT'), ('CoalitionAssistance','CA'), ('CoalitionSimilarity','CS')])

BAR_FILL		= 0.60
FONT_SIZE		= 6
FONT_FAMILY		= 'serif'
# DOMAIN			= 'first_response'
DOMAIN			= 'blocks_world'
PLANNER			= 'colin2'
# PLANNER			= 'tfddownward'
# DOMAIN			= 'first_response'
COL_PAD			= 5
CSPACING		= 1
LEGEND			= False

# File names
GATHER_DATA_SCRIPT	= "scripts/gather_data.sh"
RAW_STATS			= "csv/stats.csv"
FILTERED_STATS		= "csv/stats_filtered.csv"
STATS_TABLE			= "csv/stats_table.csv"
P_TABLE				= "csv/p_table_"
PLOT_FORMATS		= ['pdf', 'svg', 'eps']
STATS_PLOT_NAME		= "plots/stats_plot"
PDF_PLOT_NAME		= "plots/pdf_plot"


# Labels
header		= ['Domain','Problem','CFA','Planner','Tool','Makespan (%)','Number of Actions (%)','Processing Time (%)','Memory Usage (%)','Planning Results (%)']

lmetrics	= header[-5:]
lmetrics	= [lmetrics[-1]]+lmetrics[:-1]

NCOL		= 4

if DOMAIN == 'first_response':
	# ltools		= ['CFP', 'PA']
	ltools		= ['CFP', 'Object', 'ObjectTime', 'CoalitionAssistance', 'CoalitionSimilarity']
	FIG_SIZE	= (3.4, 5.0)
	LABEL_OSET_RESULTS	= 0.5
	LABEL_OSET_METRICS	= -1.0

if DOMAIN == 'blocks_world':
	# ltools		= ['CFP', 'Object', 'ObjectTime', 'CoalitionAssistance', 'CoalitionSimilarity', 'PA']
	ltools		= ['ActionObjectTime', 'ActionObject', 'ActionTime', 'Action', 'ObjectTime', 'Object', 'CoalitionAssistance', 'CoalitionSimilarity', 'CFP', 'PA']
	FIG_SIZE	= (3.4, 15.0)
	LABEL_OSET_RESULTS	= 0.5
	LABEL_OSET_METRICS	= -0.6

def p_test(metrics, ltools, status):
	p_test_results = {}
	for m, metric in enumerate(metrics):
		if metric != "Planning Results (%)":
			for i, t1 in enumerate(metrics[metric]['sample'][status]):
				for j, t2 in enumerate(metrics[metric]['sample'][status]):
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

def generate_stats_table(metrics, ltools, separator=None):

	# Assembling stats_table
	stats_table = []
	trow = []

	# Header
	for h in ["Metric"] + list(reversed(ltools)):
		trow.append(h)
	stats_table.append(trow)

	# Body
	for metric in metrics:
		if metric == "Planning Results (%)":
			for f in STATUS_FLAGS:
				trow = []
				for r in ["\"%s\""%f] + ["%.*f"%(CSPACING,v) for v in reversed(metrics[metric][f])]:
					trow.append(r)
				stats_table.append(trow)
		else:

			for f in STATUS_FLAGS:
				trow = []
				content = []
				for i in reversed(range(len(metrics[metric]['mean'][f]))):
					content.append("%.*f (%.*f)"%(CSPACING,metrics[metric]['mean'][f][i],CSPACING,metrics[metric]['error'][f][i]))
				for r in ["\"%s\""%metric] + content:
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
	gridspec.GridSpec(9,1)
	numbars = len(ltools)
	bar_origin = ((1-BAR_FILL)/2)*np.ones(numbars) + np.asarray(range(numbars))

	ntools = []
	for t in ltools:
		ntools.append(TOOLS_LONG[t])

	# For each metric
	grid_ctr = 0
	for m, metric in enumerate(metrics):

		if metric in set(['Processing Time (%)','Memory Usage (%)']):
			bar_width = 0.25*BAR_FILL
			ax = plt.subplot2grid((9,1), (grid_ctr,0), rowspan=3)
			grid_ctr += 3
		else:
			bar_width = BAR_FILL
			ax = plt.subplot2grid((9,1), (grid_ctr,0))
			grid_ctr += 1

		ax.xaxis.grid(True, which='major')
		ax.set_axisbelow(True)

		shift_pos = bar_origin
		if metric != "Planning Results (%)":
			if metric in set(['Processing Time (%)','Memory Usage (%)']):
				counter = 3
				for f in STATUS_FLAGS:
					plt.barh(shift_pos+bar_width*counter, metrics[metric]['mean'][f], bar_width, color=C[3-counter], xerr=metrics[metric]['error'][f], ecolor='k')
					counter -= 1
			else:
				plt.barh(shift_pos+bar_width*0, metrics[metric]['mean']['Success (%)'], bar_width, color=C[0], xerr=metrics[metric]['error']['Success (%)'], ecolor='k')
		else:
			label_succ = []
			for f in STATUS_FLAGS:
				label_succ.append(STATUS_SHORT[f])
			barl = np.array([100.00]*len(ltools))
			bar_handle = []
			for i,f in enumerate(list(reversed(list(STATUS_FLAGS)))):
				bar_handle.append(plt.barh(shift_pos, barl, bar_width, color=C[3-i]))
				barl -= np.array(metrics[metric][f])
			plt.legend(list(reversed(bar_handle)), label_succ, loc='lower center', bbox_to_anchor=(LABEL_OSET_RESULTS,1.0), ncol=NCOL, fontsize=FONT_SIZE)
			plt.xlim([0, 100])

		plt.xlabel(metric)
		plt.yticks(bar_origin+BAR_FILL/2, ntools)
		plt.ylim([0, numbars]) 

	# Legend and ticks
	plt.tight_layout()
	for f in PLOT_FORMATS:
		plt.savefig(STATS_PLOT_NAME+'.'+f, bbox_inches='tight')

def get_stats(sample):
	if len(sample) == 0:
		return 0, 0
	mean = stat.mean(sample)
	error = stat.stdev(sample)/len(sample)**0.5
	return mean, error

# Gathering data
print 'Gathering data ...'
os.system(GATHER_DATA_SCRIPT)

# Filtering CSV file
print 'Filtering CSV file ...'
StatsFilter.filter(RAW_STATS,FILTERED_STATS,header)

# Creating database
print 'Creating database ...'
db = CsvDatabase(FILTERED_STATS)

# Stats on Problems Solved/Unsolved
print 'Stats on Problems Solved/Unsolved ...'
problem_stats = OrderedDict()
for s in tqdm(set(db.select('Problem', db.query([('Domain',DOMAIN)])))):
	problem_stats[s] = OrderedDict()
	for metric in lmetrics:
		if metric in set(['Makespan (%)','Number of Actions (%)']):
			raw_select = db.select(metric, db.query([('Domain',DOMAIN), ('Problem',s), ('Planning Results (%)','0')]), as_float=True)
			problem_stats[s][metric] = list(filter(lambda a: a > 0, raw_select))
		if metric in set(['Processing Time (%)','Memory Usage (%)']):
			raw_select = db.select(metric, db.query([('Domain',DOMAIN), ('Problem',s)]), as_float=True)
			problem_stats[s][metric] = list(filter(lambda a: a > 0, raw_select))

# For each metric
print 'Processing ...'
metrics = OrderedDict()
for metric in tqdm(lmetrics):

	metrics[metric] = OrderedDict()
	metrics[metric]['sample']			= []
	for f in STATUS_FLAGS:
		metrics[metric][f]				= []
	metrics[metric]['mean']				= {}
	metrics[metric]['error']			= {}
	metrics[metric]['sample']			= {}
	for f in STATUS_FLAGS:
		metrics[metric]['mean'][f]		= []
		metrics[metric]['error'][f]		= []
		metrics[metric]['sample'][f]	= []

	# For each tool
	for tool in ltools:
		if metric == "Planning Results (%)":
			query_all = db.query([('Domain',DOMAIN),('Planner',PLANNER),('Tool',tool)])
			status = db.select('Planning Results (%)', query_all, as_integer=True)
			for f in STATUS_FLAGS:
				metrics[metric][f].append(100.0*len([k for k in status if k == STATUS_FLAGS[f]])/len(query_all))
		else:

			for f in STATUS_FLAGS:
				normalized		= []
				for p in db.select(['Problem', metric], db.query([('Domain',DOMAIN),('Planner',PLANNER),('Tool',tool),('Planning Results (%)',str(STATUS_FLAGS[f]))])):
					if len(problem_stats[p[0]][metric]) > 0:
						normalized.append(100.00*float(p[1])/stat.mean(problem_stats[p[0]][metric]) - 100.00)
				mean, error = get_stats(normalized)
				metrics[metric]['mean'][f].append(mean)
				metrics[metric]['error'][f].append(error)
				metrics[metric]['sample'][f].append(normalized)

# P-Test Tables
print 'P-Test Table ...'
for f in STATUS_FLAGS:
	with open(P_TABLE+PLANNER+'_'+STATUS_SHORT[f].replace(' ','')+'.csv', 'wb') as file:
		file.write(p_test_table(p_test(metrics,ltools,f)))

# Stats Table
print 'Stats Table ...'
with open(STATS_TABLE, 'wb') as f:
	f.write(generate_stats_table(metrics,ltools,","))

# Stats Plots
print 'Stats Plots ...'
generate_stats_plots(metrics,ltools)
