#!/usr/bin/python
import os
import matplotlib
import matplotlib.pyplot as plt
import statistics as stat
import numpy as np
from tqdm import tqdm
from tabulate import tabulate
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
TOOLS_SHORT		= OrderedDict([('PA','PA'), ('CFP','CFP'), ('Object','O'), ('ObjectTime','OT'), ('Action','A'), ('ActionTime','AT'), ('ActionObject','AO'), ('ActionObjectTime','AOT'), ('CoalitionAssistance','CA'), ('CoalitionSimilarity','CS')])

BAR_FILL		= 0.60
FONT_SIZE		= 6
FONT_FAMILY		= 'serif'

# DOMAIN			= 'first_response'
DOMAIN			= 'blocks_world'
# PLANNER			= 'tfddownward'
PLANNER			= 'colin2'
COL_PAD			= 5
CSPACING		= 1

# File names
GATHER_DATA_SCRIPT	= "scripts/gather_data.sh"
RAW_STATS			= "csv/stats.csv"
FILTERED_STATS		= "csv/stats_filtered.csv"
STATS_TABLE			= "csv/stats_table.csv"
KRUSKAL				= "csv/kruskal_"
PLOT_FORMATS		= ['pdf', 'svg', 'eps']
STATS_PLOT_NAME		= "plots/stats_plot"
PDF_PLOT_NAME		= "plots/pdf_plot"


# Labels
header		= ['Domain','Problem','CFA','Planner','Tool','Makespan (s)','Number of Actions','Processing Time (s)','Memory Usage (GB)','Planning Results (%)']

lmetrics	= header[-5:]
lmetrics	= [lmetrics[-1]]+lmetrics[:-1]

NCOL		= 4

tools		= ['ActionObjectTime', 'ActionObject', 'ActionTime', 'Action', 'ObjectTime', 'Object', 'CoalitionAssistance', 'CoalitionSimilarity', 'CFP', 'PA']
FIG_SIZE	= (10.0, 5.0)
LABEL_OSET_RESULTS	= 0.5
LABEL_OSET_METRICS	= -0.6

tools_short = [TOOLS_SHORT[t] for t in tools]

def table_to_string(table, separator=None):

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

def compute_kruskal(metrics, tools, status):
	ret_var = {}
	for m, metric in enumerate(metrics):
		if metric != "Planning Results (%)":
			for i, t1 in enumerate(metrics[metric]['sample'][status]):
				for j, t2 in enumerate(metrics[metric]['sample'][status]):
					if j != i:
						if (tools_short[i], tools_short[j]) not in ret_var:
							ret_var[(tools_short[i], tools_short[j])] = {}
						if set(t1).issubset(t2) or set(t2).issubset(t1):
							aux = (0.0,1.0)
						else:
							aux = stats.kruskal(t1,t2)
						ret_var[(tools_short[i], tools_short[j])][metric] = aux
	return ret_var

def generate_kruskal_table(kruskal_results):

	# Assembling Kruskal table
	ret_var = []

	# Header 1
	trow = []
	trow.append('Pair')
	trow.append('Pair')
	for r in kruskal_results:
		for h in kruskal_results[r]:
			trow.append("%s" % h)
			trow.append("%s" % h)
		break
	ret_var.append(trow)

	# Header 2
	trow = []
	trow.append('Tool A')
	trow.append('Tool B')
	for r in kruskal_results:
		for h in kruskal_results[r]:
			trow.append("H")
			trow.append("p")
		break
	ret_var.append(trow)

	# Body
	for i, t1 in enumerate(reversed(tools_short)):
		for j, t2 in enumerate(reversed(tools_short)):
			if i < j:
				trow = []
				trow.append('%s' % t1)
				trow.append('%s' % t2)
				for m in kruskal_results[(t1,t2)]:
					for entry in kruskal_results[(t1,t2)][m]:
						trow.append("%0.4f" % entry)
				ret_var.append(trow)


	return ret_var

def generate_stats_table(metrics, tools):

	# Assembling stats table
	ret_var = []
	trow = []

	# Header
	for h in ["Metric"] + list(reversed(tools_short)):
		trow.append(h)
	ret_var.append(trow)

	# Body
	for metric in metrics:
		if metric == "Planning Results (%)":
			for f in STATUS_FLAGS:
				trow = []
				for r in ["\"%s\""%f] + ["%.*f"%(CSPACING,v) for v in reversed(metrics[metric][f])]:
					trow.append(r)
				ret_var.append(trow)
		else:
			for f in STATUS_FLAGS:
				trow = []
				content = []
				for i in reversed(range(len(metrics[metric]['mean'][f]))):
					content.append("%.*f (%.*f)"%(CSPACING,metrics[metric]['mean'][f][i],CSPACING,metrics[metric]['error'][f][i]))
				for r in ["\"%s\""%metric] + content:
					trow.append(r)
				ret_var.append(trow)

	return ret_var

def generate_stats_plots(metrics,tools):
	plt.figure(figsize=FIG_SIZE)
	matplotlib.rcParams.update({'font.size': FONT_SIZE})
	matplotlib.rcParams.update({'font.family': FONT_FAMILY})
	gridspec.GridSpec(9,1)
	numbars = len(tools)
	bar_origin = ((1-BAR_FILL)/2)*np.ones(numbars) + np.asarray(range(numbars))

	# For each metric
	grid_ctr = 0
	for m, metric in enumerate(metrics):

		if metric in set(['Processing Time (s)','Memory Usage (GB)']):
			bar_width = 0.25*BAR_FILL
		else:
			bar_width = BAR_FILL

		if metric in set(['Processing Time (s)']):
			ax = plt.subplot2grid((3,3), (0,1), rowspan=3)
		elif metric in set(['Memory Usage (GB)']):
			ax = plt.subplot2grid((3,3), (0,2), rowspan=3)
		else:
			ax = plt.subplot2grid((3,3), (grid_ctr,0))
			grid_ctr += 1

		ax.xaxis.grid(True, which='major')
		ax.set_axisbelow(True)

		shift_pos = bar_origin
		if metric == "Planning Results (%)":
			label_succ = []
			for f in STATUS_FLAGS:
				label_succ.append(STATUS_SHORT[f])
			barl = np.array([100.00]*len(tools))
			bar_handle = []
			for i,f in enumerate(list(reversed(list(STATUS_FLAGS)))):
				bar_handle.append(plt.barh(shift_pos, barl, bar_width, color=C[3-i]))
				barl -= np.array(metrics[metric][f])
			plt.legend(list(reversed(bar_handle)), label_succ, loc='lower center', bbox_to_anchor=(LABEL_OSET_RESULTS,1.0), ncol=NCOL, fontsize=FONT_SIZE)
			plt.xlim([0, 100])
		else:
			if metric in set(['Processing Time (s)','Memory Usage (GB)']):
				counter = 3
				for f in STATUS_FLAGS:
					plt.barh(shift_pos+bar_width*counter, metrics[metric]['mean'][f], bar_width, color=C[3-counter], xerr=metrics[metric]['error'][f], ecolor='k')
					counter -= 1
				if metric in set(['Processing Time (s)']):
					plt.xlim([0, 3600])
				if metric in set(['Memory Usage (GB)']):
					plt.xlim([0, 120])
			else:
				plt.barh(shift_pos+bar_width*0, metrics[metric]['mean']['Success (%)'], bar_width, color=C[0], xerr=metrics[metric]['error']['Success (%)'], ecolor='k')

		plt.xlabel(metric)
		plt.yticks(bar_origin+BAR_FILL/2, tools_short)
		plt.ylim([0, numbars]) 

	# Legend and ticks
	plt.tight_layout()
	for f in PLOT_FORMATS:
		plt.savefig(STATS_PLOT_NAME+'.'+f, bbox_inches='tight')

def get_stats(sample):
	if len(sample) < 2:
		return float('nan'), float('nan')
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
	for t in tools:
		if metric == "Planning Results (%)":
			query_all = db.query([('Domain',DOMAIN),('Planner',PLANNER),('Tool',t)])
			status = db.select('Planning Results (%)', query_all, as_integer=True)
			for f in STATUS_FLAGS:
				metrics[metric][f].append(100.0*len([k for k in status if k == STATUS_FLAGS[f]])/len(query_all))
		else:
			for f in STATUS_FLAGS:
				sample = db.select(metric, db.query([('Domain',DOMAIN),('Planner',PLANNER),('Tool',t),('Planning Results (%)',str(STATUS_FLAGS[f]))]), as_float=True)
				mean, error = get_stats(sample)
				metrics[metric]['mean'][f].append(mean)
				metrics[metric]['error'][f].append(error)
				metrics[metric]['sample'][f].append(sample)

# Kruskal Tables
print 'Kruskal Table ...'
for f in OrderedDict([('Success (%)',0), ('Nonexecutable (%)',1), ('Time Fail (%)',124), ('Memory Fail (%)',134)]):
	with open(KRUSKAL+PLANNER+'_'+STATUS_SHORT[f].replace(' ','')+'.csv', 'wb') as file:
		kruss = compute_kruskal(metrics,tools,f)
		kruskal_table = generate_kruskal_table(kruss)
		file.write(table_to_string(kruskal_table,','))

# Stats Table
print 'Stats Table ...'
with open(STATS_TABLE, 'wb') as file:
	stats_table = generate_stats_table(metrics,tools)
	print table_to_string(stats_table)
	file.write(table_to_string(stats_table,','))
	# print tabulate(stats_table, headers="firstrow", tablefmt="latex")

# Stats Plots
print 'Stats Plots ...'
generate_stats_plots(metrics,tools)
