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


# SPREAD = 'STDEV'
SPREAD = 'CI'


STATUSES	= OrderedDict([
							('Success (%)',			OrderedDict([	('short', 'Success'),	('code', 0),	('color', (0.000, 0.447, 0.741))	])), # Blue
							('Nonexecutable (%)',	OrderedDict([	('short', 'Nonexec'),	('code', 1),	('color', (0.850, 0.325, 0.098))	])), # Tomato
							('Time Fail (%)',		OrderedDict([	('short', 'Time Fail'),	('code', 124),	('color', (0.929, 0.694, 0.125))	])), # Orange
							('Memory Fail (%)',		OrderedDict([	('short', 'Mem Fail'),	('code', 134),	('color', (0.929, 0.894, 0.325))	])), # Yellow
						])

TOOLS		= OrderedDict([
							# ('PA',					OrderedDict([	('reg', 'PA'),		('tex','PA')			])),
							('CFP',					OrderedDict([	('reg', 'CFP'),		('tex','CFP')			])),
							('CoalitionSimilarity',	OrderedDict([	('reg', 'CS'),		('tex','CS')			])),
							('CoalitionAssistance',	OrderedDict([	('reg', 'CA'),		('tex','CA')			])),
							('Object',				OrderedDict([	('reg', 'O'),		('tex',r'\textbf{O}')	])),
							('Action',				OrderedDict([	('reg', 'A'),		('tex',r'\textbf{A}')	])),
							('ActionObject',		OrderedDict([	('reg', 'AO'),		('tex',r'\textbf{AO}')	])),
							('ObjectTime',			OrderedDict([	('reg', 'OT'),		('tex',r'\textbf{OT}')	])),
							('ActionTime',			OrderedDict([	('reg', 'AT'),		('tex',r'\textbf{AT}')	])),
							('ActionObjectTime',	OrderedDict([	('reg', 'AOT'),		('tex',r'\textbf{AOT}')	])),
						])

METRICS		= OrderedDict([
							('Planning Results (%)',	'a) Planning results'),
							('Makespan (s)',			'b) Makespan'),
							('Number of Actions',		'c) Number of actions'),
							('Processing Time (s)',		'd) Processing time'),
							('Memory Usage (GB)',		'e) Memory usage'),
						])


# Labels
file_header		= ['Domain','Problem','CFA','Planner','Tool', 'Planning Results (%)', 'Makespan (s)', 'Number of Actions', 'Processing Time (s)', 'Memory Usage (GB)']


BAR_FILL		= 0.60
FONT_SIZE		= 7
FONT_FAMILY		= 'serif'

DOMAIN			= 'first_response'
# DOMAIN			= 'blocks_world'
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
PLOT_FORMATS		= ['pdf', 'eps']
STATS_PLOT_NAME		= "plots/stats_plot"
PDF_PLOT_NAME		= "plots/pdf_plot"

NCOL		= 2

FIG_SIZE	= (9.0, 5.0)
LABEL_OSET_RESULTS	= 0.5
LABEL_OSET_METRICS	= -0.6

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

def compute_kruskal(metrics, status):
	ret_var = OrderedDict()
	for metric in metrics.keys():
		if metric != "Planning Results (%)":
			for t1 in metrics[metric]['sample'][status]:
				for t2 in metrics[metric]['sample'][status]:
					if t1 != t2:
						tool_pair = (TOOLS[t1]['reg'], TOOLS[t2]['reg'])
						if tool_pair not in ret_var:
							ret_var[tool_pair] = OrderedDict()
						if set(metrics[metric]['sample'][status][t1]).issubset(metrics[metric]['sample'][status][t2]) or set(metrics[metric]['sample'][status][t2]).issubset(metrics[metric]['sample'][status][t1]):
							ret_var[tool_pair][metric] = (0.0,1.0)
						else:
							ret_var[tool_pair][metric] = stats.kruskal(metrics[metric]['sample'][status][t1],metrics[metric]['sample'][status][t2])

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
	for i, t1 in enumerate(TOOLS.values()):
		for j, t2 in enumerate(TOOLS.values()):
			if i < j:
				trow = []
				trow.append('%s' % t1['reg'])
				trow.append('%s' % t2['reg'])
				for m in kruskal_results[(t1['reg'],t2['reg'])]:
					for entry in kruskal_results[(t1['reg'],t2['reg'])][m]:
						trow.append("%0.4f" % entry)
				ret_var.append(trow)

	return ret_var

def generate_stats_table(metrics):

	# Assembling stats table
	ret_var = []
	trow = []

	# Header
	for h in ["Metric"] + [k['reg'] for k in TOOLS.values()]:
		trow.append(h)
	ret_var.append(trow)

	# Body
	for metric in metrics:
		for f in STATUSES:
			if metric == "Planning Results (%)":
				trow = ["\"%s\""%f]
			else:
				trow = ["\"%s\""%metric]
			for t in TOOLS.keys():
				if metric == "Planning Results (%)":
					trow.append("%.*f"%(CSPACING,metrics[metric][f][t]))
				else:
					trow.append("%.*f (%.*f)"%(CSPACING,metrics[metric]['mean'][f][t],CSPACING,metrics[metric]['error'][f][t]))
			ret_var.append(trow)
	return ret_var

def generate_stats_plots(metrics):
	plt.figure(figsize=FIG_SIZE)
	matplotlib.rcParams.update({'font.size': FONT_SIZE})
	matplotlib.rcParams.update({'font.family': FONT_FAMILY})
	matplotlib.rc('text', usetex=True)
	gridspec.GridSpec(9,1)
	numbars = len(TOOLS)
	bar_origin = ((1-BAR_FILL)/2)*np.ones(numbars) + np.asarray(range(numbars))

	# For each metric
	grid_ctr = 0
	for m, metric in enumerate(metrics):

		if metric in set(['Processing Time (s)','Memory Usage (GB)']):
			bar_width = 0.33*BAR_FILL
		else:
			bar_width = BAR_FILL

		if metric in set(['Processing Time (s)']):
			ax = plt.subplot2grid((3,3), (0,1), rowspan=3)
		elif metric in set(['Memory Usage (GB)']):
			ax = plt.subplot2grid((3,3), (0,2), rowspan=3)
		else:
			ax = plt.subplot2grid((3,3), (grid_ctr,0))
			grid_ctr += 1

		plt.title(METRICS[metric]+' for each tool.', loc='left')
		ax.xaxis.grid(True, which='major')
		ax.set_axisbelow(True)

		shift_pos = bar_origin
		if metric == "Planning Results (%)":
			label_succ = []
			for f in STATUSES:
				label_succ.append(STATUSES[f]['short'])
			barl = np.array([100.00]*len(TOOLS))
			bar_handle = []
			for i,f in enumerate(list(reversed(STATUSES.keys()))):
				bar_handle.append(plt.barh(shift_pos, barl, bar_width, color=STATUSES[f]['color']))
				barl -= np.array(list(reversed(metrics[metric][f].values())))
			plt.legend(list(reversed(bar_handle)), label_succ, loc='lower center', bbox_to_anchor=(LABEL_OSET_RESULTS,1.2), ncol=NCOL, fontsize=FONT_SIZE)
			plt.xlim([0, 100])
		else:
			if metric in set(['Processing Time (s)','Memory Usage (GB)']):
				if metric in set(['Processing Time (s)']):
					tool_plot = ['Success (%)', 'Nonexecutable (%)', 'Memory Fail (%)']
				if metric in set(['Memory Usage (GB)']):
					tool_plot = ['Success (%)', 'Nonexecutable (%)', 'Time Fail (%)']
				counter = 2
				for f in tool_plot:
					means	= list(reversed(metrics[metric]['mean'][f].values()))
					errors	= list(reversed(metrics[metric]['error'][f].values()))
					plt.barh(shift_pos+bar_width*counter, means, bar_width, color=STATUSES[f]['color'], xerr=errors, ecolor='k')
					counter -= 1
			else:
				means	= list(reversed(metrics[metric]['mean']['Success (%)'].values()))
				errors	= list(reversed(metrics[metric]['error']['Success (%)'].values()))
				plt.barh(shift_pos+bar_width*0, means, bar_width, color=STATUSES['Success (%)']['color'], xerr=errors, ecolor='k')
		ax.set_xlim(left=0, right=None)

		plt.xlabel(metric.replace('%','\%'))
		plt.yticks(bar_origin+BAR_FILL/2, list(reversed([k['tex'] for k in TOOLS.values()])))
		plt.ylim([0, numbars]) 

	# Legend and ticks
	plt.tight_layout()
	for f in PLOT_FORMATS:
		plt.savefig(STATS_PLOT_NAME+'.'+f, bbox_inches='tight')

def get_stats(sample):
	if len(sample) < 2:
		return float('nan'), float('nan')
	mean = stat.mean(sample)
	if SPREAD == 'STDEV':
		error = stat.stdev(sample)
	if SPREAD == 'CI':
		error = 1.96*stat.stdev(sample)/len(sample)**0.5
	return mean, error

# Gathering data
print 'Gathering data ...'
os.system(GATHER_DATA_SCRIPT)

# Filtering CSV file
print 'Filtering CSV file ...'
StatsFilter.filter(RAW_STATS,FILTERED_STATS,file_header)

# Creating database
print 'Creating database ...'
db = CsvDatabase(FILTERED_STATS)

# For each metric
print 'Processing ...'
metrics = OrderedDict()
for metric in tqdm(METRICS.keys()):
	metrics[metric] = OrderedDict()
	metrics[metric]['mean']				= OrderedDict()
	metrics[metric]['error']			= OrderedDict()
	metrics[metric]['sample']			= OrderedDict()
	for f in STATUSES:
		metrics[metric][f]				= OrderedDict()
		metrics[metric]['mean'][f]		= OrderedDict()
		metrics[metric]['error'][f]		= OrderedDict()
		metrics[metric]['sample'][f]	= OrderedDict()

	# For each tool
	for t in TOOLS.keys():
		if metric == "Planning Results (%)":
			query_all	= db.query([('Domain',DOMAIN),('Planner',PLANNER),('Tool',t)])
			status		= db.select('Planning Results (%)', query_all, as_integer=True)
			for f in STATUSES:
				metrics[metric][f][t] = 100.0*len([k for k in status if k == STATUSES[f]['code']])/len(query_all)
		else:
			for f in STATUSES:
				sample = db.select(metric, db.query([('Domain',DOMAIN),('Planner',PLANNER),('Tool',t),('Planning Results (%)',str(STATUSES[f]['code']))]), as_float=True)
				mean, error = get_stats(sample)
				metrics[metric]['mean'][f][t]	= mean
				metrics[metric]['error'][f][t]	= error
				metrics[metric]['sample'][f][t]	= sample

# Kruskal Tables
print 'Kruskal Table ...'
for f in STATUSES:
	with open(KRUSKAL+PLANNER+'_'+STATUSES[f]['short'].replace(' ','')+'.csv', 'wb') as file:
		kruss = compute_kruskal(metrics,f)
		kruskal_table = generate_kruskal_table(kruss)
		file.write(table_to_string(kruskal_table,','))

# Stats Table
print 'Stats Table ...'
with open(STATS_TABLE, 'wb') as file:
	stats_table = generate_stats_table(metrics)
	print table_to_string(stats_table)
	file.write(table_to_string(stats_table,','))
	# print tabulate(stats_table, headers="firstrow", tablefmt="latex")

# Stats Plots
print 'Stats Plots ...'
generate_stats_plots(metrics)
