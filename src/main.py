#!/usr/bin/python
import os
import matplotlib
import matplotlib.pyplot as plt
import statistics as stat
import numpy as np
from collections import OrderedDict
from scipy import stats
from CsvDatabase import *
from StatsFilter import *

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

		(0.000, 0.000, 0.750), # Blue
		(1.000, 0.000, 0.000), # Tomato
		(1.000, 0.500, 0.000), # Orange
		(1.000, 1.000, 0.000), # Yellow
	]

STATUS_FLAGS	= OrderedDict([('Memory Fail (%)',134), ('Time Fail (%)',124), ('Nonexecutable (%)',1), ('Success (%)',0)])
STATUS_SHORT	= OrderedDict([('Memory Fail (%)','Mem Fail'), ('Time Fail (%)','Time Fail'), ('Nonexecutable (%)','Nonex'), ('Success (%)','Success')])
TOOLS_LONG		= OrderedDict([('CFP','CFP'), ('Object','Object'), ('ObjectTime','Object-Temporal'), ('CoalitionAssistance','Coalition Assistance'), ('CoalitionSimilarity','Coalition Similarity'), ('PA','Planning Alone')])

BAR_FILL		= 0.60
FONT_SIZE		= 8
FONT_FAMILY		= 'serif'
DOMAIN			= 'blocks_world'
# DOMAIN			= 'blocks_world'
# DOMAIN			= 'first_response'
COL_PAD			= 5
CSPACING		= 1
LEGEND			= False

# File names
GATHER_DATA_SCRIPT	= "scripts/gather_data.sh"
RAW_STATS			= "csv/stats.csv"
FILTERED_STATS		= "csv/stats_filtered.csv"
STATS_TABLE			= "csv/stats_table.csv"
P_TABLE				= "csv/p_table"
PLOT_FORMATS		= ['pdf', 'svg', 'eps']
STATS_PLOT_NAME		= "plots/stats_plot"
PDF_PLOT_NAME		= "plots/pdf_plot"


# Labels
header		= ['Domain','Problem','CFA','Planner','Tool','Makespan (%)','Number of Actions (%)','Processing Time (%)','Memory Usage (%)','Planning Results (%)']

lmetrics	= header[-5:]
lmetrics	= [lmetrics[-1]]+lmetrics[:-1]


if DOMAIN == 'first_response':
	lplanners	= ['colin2']
	ltools		= ['CFP', 'Object', 'ObjectTime', 'CoalitionAssistance', 'CoalitionSimilarity']
	FIG_SIZE	= (4, 6)
	LABEL_OSET	= -1.0

if DOMAIN == 'blocks_world':
	lplanners	= ['tfddownward', 'colin2']
	ltools		= ['CFP', 'Object', 'ObjectTime', 'CoalitionAssistance', 'CoalitionSimilarity', 'PA']
	FIG_SIZE	= (4, 9)
	LABEL_OSET	= -0.6

# Neat Names
NPLANNERS = {'tfddownward': 'TFD', 'colin2': 'COLIN'}

def p_test(metrics, ltools, planner):
	p_test_results = {}
	for m, metric in enumerate(metrics):
		if metric != "Planning Results (%)":
			for i, t1 in enumerate(metrics[metric][planner]['sample']):
				for j, t2 in enumerate(metrics[metric][planner]['sample']):
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

	ntools = []
	for t in ltools:
		ntools.append(TOOLS_LONG[t])

	# For each metric
	for m, metric in enumerate(metrics):
		lplanners = []
		for p in metrics[metric]:
			lplanners.append(NPLANNERS[p])
		bar_width = BAR_FILL/len(lplanners)

		ax = plt.subplot(subplot_pfix+m+1)
		ax.xaxis.grid(True, which='major')
		ax.set_axisbelow(True)

		# For each planner
		for p, planner in enumerate(metrics[metric]):

			shift_pos = bar_origin+bar_width*p
			if metric != "Planning Results (%)":
				plt.barh(shift_pos, metrics[metric][planner]['mean'], bar_width, color=C[p], xerr=metrics[metric][planner]['error'], ecolor='k')
			else:
				label_succ = []
				for lp in lplanners:
					prefix = ""
					if len(lplanners) > 1:
						prefix = lp+" "
					for f in STATUS_FLAGS:
						label_succ.append(prefix+f)
				barl = np.array([100.00]*len(ltools))
				for i,f in enumerate(list(STATUS_FLAGS)):
					plt.barh(shift_pos, barl, bar_width, color=S[4*p+(3-i)])
					barl -= np.array(metrics[metric][planner][f])
				plt.legend(label_succ, loc='lower center', bbox_to_anchor=(0.3,1.0), ncol=2, fontsize=FONT_SIZE)
				plt.xlim([0, 100]) 

		plt.xlabel(metric)
		plt.yticks(bar_origin+BAR_FILL/2, ntools)
		plt.ylim([0, numbars]) 

		if len(lplanners) > 1 and m == len(metrics)-1:
			plt.legend(lplanners, loc='lower center', bbox_to_anchor=(0.5,LABEL_OSET), ncol=2, fontsize=FONT_SIZE)

	# Legend and ticks
	plt.tight_layout()
	for f in PLOT_FORMATS:
		plt.savefig(STATS_PLOT_NAME+'.'+f, bbox_inches='tight')

def generate_pdf_plots(metrics,ltools):
	plt.figure(figsize=FIG_SIZE)
	matplotlib.rcParams.update({'font.size': FONT_SIZE})
	matplotlib.rcParams.update({'font.family': FONT_FAMILY})
	subplot_pfix = 10 + 100*len(metrics)

	# For each metric
	for m, metric in enumerate(metrics):
		if metric != "Planning Results (%)":

			lplanners = []
			for p in metrics[metric]:
				lplanners.append(NPLANNERS[p])

			ax = plt.subplot(subplot_pfix+m+1)
			ax.yaxis.grid(True, which='major')
			ax.set_axisbelow(True)

			# Ranges
			max_range = 0
			for planner in metrics[metric]:
				for i, tool in enumerate(metrics[metric][planner]['sample']):
					max_range = max(max(tool),max_range)

			# For each planner
			for p, planner in enumerate(metrics[metric]):
				for i, t in enumerate(metrics[metric][planner]['kde']):
					t_range = np.linspace(0,1.5*max_range,100)
					plt.plot(t_range,t(t_range))

			plt.xlabel(metric)

		if m == len(metrics)-1:
			plt.legend(ltools, loc='lower center', bbox_to_anchor=(0.5,-1.5), ncol=2, fontsize=FONT_SIZE)

	# Legend and ticks
	plt.tight_layout()
	for f in PLOT_FORMATS:
		plt.savefig(PDF_PLOT_NAME+'.'+f, bbox_inches='tight')

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

# Stats on Problems Solved
problems_stats = {}
for s in set(db.select('Problem', db.query([('Domain',DOMAIN), ('Planning Results (%)','0')]))):
	problems_stats[s] = {}
	for metric in lmetrics:
		if metric != "Planning Results (%)":
			problems_stats[s][metric] = db.select(metric, db.query([('Domain',DOMAIN), ('Planning Results (%)','0'), ('Problem',s)]), as_float=True)

# For each metric
metrics = OrderedDict()
for metric in lmetrics:

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
		metrics[metric][planner]['sample']				= []
		metrics[metric][planner]['kde']					= []
		for tool in ltools:
			if metric == "Planning Results (%)":
				query_all = db.query([('Domain',DOMAIN),('Planner',planner),('Tool',tool)])
				status = db.select('Planning Results (%)', query_all, as_integer=True)
				for f in STATUS_FLAGS:
					metrics[metric][planner][f].append(100.0*len([k for k in status if k == STATUS_FLAGS[f]])/len(query_all))
			else:
				normalized = []
				for p in db.select(['Problem', metric], db.query([('Domain',DOMAIN),('Planner',planner),('Tool',tool),('Planning Results (%)','0')])):
					normalized.append(100.00*float(p[1])/min(problems_stats[p[0]][metric]) - 100.00)
				mean, error = get_stats(normalized)
				metrics[metric][planner]['mean'].append(mean)
				metrics[metric][planner]['error'].append(error)
				metrics[metric][planner]['sample'].append(normalized)
				metrics[metric][planner]['kde'].append(stats.gaussian_kde(normalized))

# P-Test Table
for p in lplanners:
	with open(P_TABLE+'_'+p+'.csv', 'wb') as f:
		f.write(p_test_table(p_test(metrics,ltools,p)))

# Stats Table
with open(STATS_TABLE, 'wb') as f:
	f.write(generate_stats_table(metrics,ltools,","))

# Stats Plots
generate_stats_plots(metrics,ltools)

# PDF Plots
generate_pdf_plots(metrics,ltools)

