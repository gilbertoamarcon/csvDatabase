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
# DOMAIN			= 'first_response'
COL_PAD			= 5
CSPACING		= 1
LEGEND			= False

# File names
GATHER_DATA_SCRIPT	= "scripts/gather_data.sh"
RAW_STATS			= "csv/stats.csv"
FILTERED_STATS		= "csv/stats_filtered.csv"
STATS_TABLE			= "csv/stats_table.csv"
P_TABLE				= "csv/P_TABLE"
PLOT_FORMATS		= ['pdf', 'svg', 'eps']
STATS_PLOT_NAME		= "plots/stats_plot"
PDF_PLOT_NAME		= "plots/pdf_plot"


# Labels
header		= ['Domain','Problem','CFA','Planner','Tool','Makespan (%)','Number of Actions (%)','Processing Time (%)','Memory Usage (%)','Planning Results (%)']

lmetrics	= header[-5:]
lmetrics	= [lmetrics[-1]]+lmetrics[:-1]

NCOL		= 4

if DOMAIN == 'first_response':
	lplanners	= ['colin2']
	# ltools		= ['CFP', 'PA']
	ltools		= ['CFP', 'Object', 'ObjectTime', 'CoalitionAssistance', 'CoalitionSimilarity']
	FIG_SIZE	= (3.4, 5.0)
	LABEL_OSET_RESULTS	= 0.5
	LABEL_OSET_METRICS	= -1.0

if DOMAIN == 'blocks_world':
	# lplanners	= ['tfddownward', 'colin2']
	lplanners	= ['colin2']
	# ltools		= ['CFP', 'Object', 'ObjectTime', 'CoalitionAssistance', 'CoalitionSimilarity', 'PA']
	ltools		= ['ActionObjectTime', 'ActionObject', 'ActionTime', 'Action', 'ObjectTime', 'Object', 'CoalitionAssistance', 'CoalitionSimilarity', 'CFP', 'PA']
	FIG_SIZE	= (3.4, 15.0)
	LABEL_OSET_RESULTS	= 0.5
	LABEL_OSET_METRICS	= -0.6

# Neat Names
NPLANNERS = {'tfddownward': 'TFD', 'colin2': 'COLIN'}

# def p_test(metrics, ltools, planner):
# 	p_test_results = {}
# 	for m, metric in enumerate(metrics):
# 		if metric != "Planning Results (%)":
# 			for i, t1 in enumerate(metrics[metric][planner]['sample']):
# 				for j, t2 in enumerate(metrics[metric][planner]['sample']):
# 					if j > i:
# 						if (ltools[i], ltools[j]) not in p_test_results:
# 							p_test_results[(ltools[i], ltools[j])] = {}
# 						p_test_results[(ltools[i], ltools[j])][metric] = stats.kruskal(t1,t2)
# 	return p_test_results

# def p_test_table(p_test_results):
# 	ret_var = ""
# 	for p in p_test_results:
# 		ret_var += 'Pair,'
# 		for m in p_test_results[p]:
# 			ret_var += "%s," % m
# 			ret_var += "%s," % m
# 		ret_var += "\n"
# 		break
# 	for p in p_test_results:
# 		ret_var += '\"%s-%s\",' % p
# 		for m in p_test_results[p]:
# 			ret_var += "%0.4f,%0.4f," % p_test_results[p][m]
# 		ret_var += "\n"
# 	return ret_var

# def generate_stats_table(metrics, ltools, separator=None):

# 	# Assembling stats_table
# 	stats_table = []
# 	trow = []

# 	# Header
# 	for h in ["Metric", "Planner"] + ltools:
# 		trow.append(h)
# 	stats_table.append(trow)

# 	# Body
# 	for metric in metrics:
# 		for planner in metrics[metric]:
# 			if metric == "Planning Results (%)":
# 				succ = ['Success (%)', 'Nonexecutable (%)', 'Time Fail (%)', 'Memory Fail (%)']
# 				for s in succ:
# 					trow = []
# 					for r in ["\"%s\""%s, NPLANNERS[planner]] + ["%.*f"%(CSPACING,v) for v in metrics[metric][planner][s]]:
# 						trow.append(r)
# 					stats_table.append(trow)
# 			else:
# 				trow = []
# 				num_elements = len(metrics[metric][planner]['mean'])
# 				content = []
# 				for i in range(num_elements):
# 					content.append("%.*f(%.*f)"%(CSPACING,metrics[metric][planner]['mean'][i],CSPACING,metrics[metric][planner]['error'][i]))
# 				for r in ["\"%s\""%metric, NPLANNERS[planner]] + content:
# 					trow.append(r)
# 				stats_table.append(trow)
	
# 	# Getting column widths
# 	if separator is None:
# 		col_widths = OrderedDict()
# 		for j in range(len(stats_table[0])):
# 			col_width = 0
# 			for e in stats_table:
# 				col_width = max(len(e[j]),col_width)
# 			col_widths[j] = col_width+COL_PAD

# 	# Lists to string
# 	ret_var = ""
# 	for i in range(len(stats_table)):
# 		for j in range(len(stats_table[0])):
# 			if separator is None:
# 				ret_var += "% *s" % (col_widths[j],stats_table[i][j])
# 			else:
# 				ret_var += "%s%s" % (stats_table[i][j],separator)
# 		ret_var += "\n"
# 	return ret_var

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
		lplanners = []
		for p in metrics[metric]:
			lplanners.append(NPLANNERS[p])

		if metric in set(['Processing Time (%)','Memory Usage (%)']):
			bar_width = 0.25*BAR_FILL/len(lplanners)
			ax = plt.subplot2grid((9,1), (grid_ctr,0), rowspan=3)
			grid_ctr += 3
		else:
			bar_width = BAR_FILL/len(lplanners)
			ax = plt.subplot2grid((9,1), (grid_ctr,0))
			grid_ctr += 1

		ax.xaxis.grid(True, which='major')
		ax.set_axisbelow(True)

		# For each planner
		for p, planner in enumerate(metrics[metric]):

			shift_pos = bar_origin+bar_width*p
			if metric != "Planning Results (%)":
				if metric in set(['Processing Time (%)','Memory Usage (%)']):
					plt.barh(shift_pos+bar_width*3, metrics[metric][planner]['mean'],				bar_width, color=C[0], xerr=metrics[metric][planner]['error'], ecolor='k')
					plt.barh(shift_pos+bar_width*2, metrics[metric][planner]['mean_nonex_fail'],	bar_width, color=C[1], xerr=metrics[metric][planner]['error_nonex_fail'], ecolor='k')
					plt.barh(shift_pos+bar_width*1, metrics[metric][planner]['mean_time_fail'],		bar_width, color=C[2], xerr=metrics[metric][planner]['error_time_fail'], ecolor='k')
					plt.barh(shift_pos+bar_width*0, metrics[metric][planner]['mean_mem_fail'],		bar_width, color=C[3], xerr=metrics[metric][planner]['error_mem_fail'], ecolor='k')
					# plt.legend([STATUS_SHORT[k] for k in list(STATUS_FLAGS)], loc='lower center', bbox_to_anchor=(LABEL_OSET_RESULTS,1.0), ncol=NCOL, fontsize=FONT_SIZE)
				else:
					plt.barh(shift_pos+bar_width*0, metrics[metric][planner]['mean'], bar_width, color=C[0], xerr=metrics[metric][planner]['error'], ecolor='k')
			else:
				label_succ = []
				for lp in lplanners:
					prefix = ""
					if len(lplanners) > 1:
						prefix = lp+" "
					for f in STATUS_FLAGS:
						label_succ.append(prefix+STATUS_SHORT[f])
				barl = np.array([100.00]*len(ltools))
				bar_handle = []
				for i,f in enumerate(list(reversed(list(STATUS_FLAGS)))):
					bar_handle.append(plt.barh(shift_pos, barl, bar_width, color=C[4*p+(3-i)]))
					barl -= np.array(metrics[metric][planner][f])
				plt.legend(list(reversed(bar_handle)), label_succ, loc='lower center', bbox_to_anchor=(LABEL_OSET_RESULTS,1.0), ncol=NCOL, fontsize=FONT_SIZE)
				plt.xlim([0, 100])

		plt.xlabel(metric)
		plt.yticks(bar_origin+BAR_FILL/2, ntools)
		plt.ylim([0, numbars]) 

		if len(lplanners) > 1 and m >= 1:
			plt.legend(reversed(lplanners), loc='best', fontsize=FONT_SIZE)

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

	# For each planner
	metrics[metric] = OrderedDict()
	for planner in lplanners:
		metrics[metric][planner] = OrderedDict()
		metrics[metric][planner]['Success (%)']			= []
		metrics[metric][planner]['Nonexecutable (%)']	= []
		metrics[metric][planner]['Time Fail (%)']		= []
		metrics[metric][planner]['Memory Fail (%)']		= []
		metrics[metric][planner]['mean']				= []
		metrics[metric][planner]['error']				= []
		metrics[metric][planner]['mean_time_fail']		= []
		metrics[metric][planner]['error_time_fail']		= []
		metrics[metric][planner]['mean_mem_fail']		= []
		metrics[metric][planner]['error_mem_fail']		= []
		metrics[metric][planner]['mean_nonex_fail']		= []
		metrics[metric][planner]['error_nonex_fail']	= []
		metrics[metric][planner]['sample']				= []
		for tool in ltools:
			if metric == "Planning Results (%)":
				query_all = db.query([('Domain',DOMAIN),('Planner',planner),('Tool',tool)])
				status = db.select('Planning Results (%)', query_all, as_integer=True)
				for f in STATUS_FLAGS:
					metrics[metric][planner][f].append(100.0*len([k for k in status if k == STATUS_FLAGS[f]])/len(query_all))
			else:
				normalized_success		= []
				normalized_time_fail	= []
				normalized_mem_fail		= []
				normalized_nonex_fail	= []
				for p in db.select(['Problem', metric], db.query([('Domain',DOMAIN),('Planner',planner),('Tool',tool),('Planning Results (%)','0')])):
					if len(problem_stats[p[0]][metric]) > 0:
						normalized_success.append(100.00*float(p[1])/stat.mean(problem_stats[p[0]][metric]) - 100.00)
				for p in db.select(['Problem', metric], db.query([('Domain',DOMAIN),('Planner',planner),('Tool',tool),('Planning Results (%)','124')])):
					if len(problem_stats[p[0]][metric]) > 0:
						normalized_time_fail.append(100.00*float(p[1])/stat.mean(problem_stats[p[0]][metric]) - 100.00)
				for p in db.select(['Problem', metric], db.query([('Domain',DOMAIN),('Planner',planner),('Tool',tool),('Planning Results (%)','134')])):
					if len(problem_stats[p[0]][metric]) > 0:
						normalized_mem_fail.append(100.00*float(p[1])/stat.mean(problem_stats[p[0]][metric]) - 100.00)
				for p in db.select(['Problem', metric], db.query([('Domain',DOMAIN),('Planner',planner),('Tool',tool),('Planning Results (%)','1')])):
					if len(problem_stats[p[0]][metric]) > 0:
						normalized_nonex_fail.append(100.00*float(p[1])/stat.mean(problem_stats[p[0]][metric]) - 100.00)
				mean, error = get_stats(normalized_success)
				metrics[metric][planner]['mean'].append(mean)
				metrics[metric][planner]['error'].append(error)
				mean, error = get_stats(normalized_nonex_fail)
				metrics[metric][planner]['mean_nonex_fail'].append(mean)
				metrics[metric][planner]['error_nonex_fail'].append(error)
				metrics[metric][planner]['sample'].append(normalized_success)
				mean, error = get_stats(normalized_time_fail)
				metrics[metric][planner]['mean_time_fail'].append(mean)
				metrics[metric][planner]['error_time_fail'].append(error)
				mean, error = get_stats(normalized_mem_fail)
				metrics[metric][planner]['mean_mem_fail'].append(mean)
				metrics[metric][planner]['error_mem_fail'].append(error)

# # P-Test Table
# print 'P-Test Table ...'
# for p in lplanners:
# 	with open(P_TABLE+'_'+p+'.csv', 'wb') as f:
# 		f.write(p_test_table(p_test(metrics,ltools,p)))

# # Stats Table
# print 'Stats Table ...'
# with open(STATS_TABLE, 'wb') as f:
# 	f.write(generate_stats_table(metrics,ltools,","))

# Stats Plots
print 'Stats Plots ...'
generate_stats_plots(metrics,ltools)
