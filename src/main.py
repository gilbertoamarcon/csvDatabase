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

# Tool sets
TOOLS_BASELINE		= ['PA', 'CFP', 'CoalitionSimilarity', 'CoalitionAssistance']
TOOLS_RP			= ['Object', 'Action', 'ActionObject', 'ObjectTime', 'ActionTime', 'ActionObjectTime']

# SPREAD			= 'STDEV'
SPREAD				= 'CI'
# PAIRWISE			= 'kw'
PAIRWISE			= 'mw'
MIN_P				= 0.01
INVALID_PAIR		= (float('nan'),float('nan'))

STATUSES			= OrderedDict([
							('Success (%)',			OrderedDict([	('short', 'Success'),	('code', 0),	('color', (0.000, 0.447, 0.741))	])), # Blue
							('Nonexecutable (%)',	OrderedDict([	('short', 'Nonexec'),	('code', 1),	('color', (0.850, 0.325, 0.098))	])), # Tomato
							('Time Fail (%)',		OrderedDict([	('short', 'Time Fail'),	('code', 124),	('color', (0.929, 0.694, 0.125))	])), # Orange
							('Memory Fail (%)',		OrderedDict([	('short', 'Mem Fail'),	('code', 134),	('color', (0.929, 0.894, 0.325))	])), # Yellow
					])

TOOLS				= OrderedDict([
							('Object',				OrderedDict([	('reg', 'O'),		('tex',r'\textbf{O}'),		('color', (1.000, 0.000, 0.000))	])),
							('Action',				OrderedDict([	('reg', 'A'),		('tex',r'\textbf{A}'),		('color', (0.000, 1.000, 0.000))	])),
							('ActionObject',		OrderedDict([	('reg', 'AO'),		('tex',r'\textbf{AO}'),		('color', (0.000, 0.000, 1.000))	])),
							('CoalitionSimilarity',	OrderedDict([	('reg', 'CS'),		('tex','CS'),				('color', (0.000, 1.000, 1.000))	])),
							('CFP',					OrderedDict([	('reg', 'CFP'),		('tex','CFP'),				('color', (1.000, 0.000, 1.000))	])),
							('ObjectTime',			OrderedDict([	('reg', 'OT'),		('tex',r'\textbf{OT}'),		('color', (1.000, 0.500, 0.000))	])),
							('ActionTime',			OrderedDict([	('reg', 'AT'),		('tex',r'\textbf{AT}'),		('color', (0.000, 0.500, 0.000))	])),
							('ActionObjectTime',	OrderedDict([	('reg', 'AOT'),		('tex',r'\textbf{AOT}'),	('color', (0.000, 0.500, 1.000))	])),
							('CoalitionAssistance',	OrderedDict([	('reg', 'CA'),		('tex','CA'),				('color', (1.000, 1.000, 0.000))	])),
							# ('PA',					OrderedDict([	('reg', 'PA'),		('tex','PA'),				('color', (0.000, 0.000, 0.000))	])),
					])

METRICS_AB				= OrderedDict([
							('Planning Results (%)',	'a) Planning results'),
							('Makespan (s)',			'b) Makespan'),
							('Number of Actions',		'c) Number of actions'),
							('Processing Time (s)',		'd) Processing time'),
							('Memory Usage (GB)',		'e) Memory usage'),
					])

METRICS				= OrderedDict([
							('Planning Results (%)',	'Planning results'),
							('Makespan (s)',			'Makespan'),
							('Number of Actions',		'Number of actions'),
							('Processing Time (s)',		'Processing time'),
							('Memory Usage (GB)',		'Memory usage'),
					])

PLANNER_DOM			= {'first_response': 'First Response', 'blocks_world': 'Blocks World', 'colin2': 'COLIN', 'tfddownward': 'TFD'}

# Labels
file_header			= ['Domain','Problem','CFA','Planner','Tool', 'Planning Results (%)', 'Makespan (s)', 'Number of Actions', 'Processing Time (s)', 'Memory Usage (GB)']

BAR_FILL			= 0.60
FONT_SIZE			= 7
FONT_FAMILY			= 'serif'

DOMAIN				= 'first_response'
# DOMAIN				= 'blocks_world'
# PLANNER				= 'tfddownward'
PLANNER				= 'colin2'
COL_PAD				= 5
CSPACING			= 1

# File names
GATHER_DATA_SCRIPT	= "scripts/gather_data.sh"
RAW_STATS			= "csv/stats.csv"
FILTERED_STATS		= "csv/stats_filtered.csv"
STATS_TABLE			= "csv/stats_"
CSV_PREFIX			= "csv/"
PLOT_FORMATS		= ['pdf', 'eps']
STATS_PLOT_NAME		= "plots/stats_"
SCATTER_PLOT_NAME	= "plots/scatter_"
BOX_PLOT_NAME		= "plots/box_"
PDF_PLOT_NAME		= "plots/pdf_plot"

NCOL				= 2

FIG_SIZE			= (9.0, 5.0)
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

def compute_general_kruskal(metrics, tools):
	ret_var = OrderedDict()
	for metric in [metric for metric in metrics.keys() if metric != "Planning Results (%)"]:
		ret_var[metric] = OrderedDict()
		for status in metrics[metric]['sample']:
			try:
				datasets = [metrics[metric]['sample'][status][k] for k in metrics[metric]['sample'][status] if k in tools]
				if len([e for e in datasets if len(e) < 2]) == 0:
					ret_var[metric][status] =  stats.kruskal(*datasets)
				else:
					raise				
			except:
				ret_var[metric][status] = INVALID_PAIR
	return ret_var

def compute_pairwise_kruskal(metrics, status):
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
							ret_var[tool_pair][metric] = INVALID_PAIR
						else:

							# Data pair
							data_set_a = metrics[metric]['sample'][status][t1]
							data_set_b = metrics[metric]['sample'][status][t2]

							# Method
							if PAIRWISE == 'kw':
								ret_var[tool_pair][metric] = stats.kruskal(data_set_a, data_set_b)
							if PAIRWISE == 'mw':
								ret_var[tool_pair][metric] = stats.mannwhitneyu(data_set_a, data_set_b)

							# Rounding up zero p-values
							if ret_var[tool_pair][metric][1] < MIN_P:
								ret_var[tool_pair][metric] = (ret_var[tool_pair][metric][0], MIN_P)

							# NaN for P >= 0.99
							if ret_var[tool_pair][metric][1] >= 0.99:
								ret_var[tool_pair][metric] = INVALID_PAIR
	return ret_var

def generate_general_kruskal_table(general_kruskal_table):

	# Header
	ret_var = [['Metric']+[status for status in general_kruskal_table[next(iter(general_kruskal_table))]]]

	# Body
	for metric in general_kruskal_table:
		trow = [metric]
		for status in general_kruskal_table[metric]:
			trow.append("%0.4f" % general_kruskal_table[metric][status][1])
		ret_var.append(trow)

	return ret_var

def generate_pairwise_kruskal_table(kruskal_results):

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
						if entry == entry:
							trow.append("%0.2f" % entry)
						else:
							trow.append("N/A")
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

		plt.title(METRICS_AB[metric]+' for each tool.', loc='left')
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
		plt.savefig(STATS_PLOT_NAME+DOMAIN+'_'+PLANNER+'.'+f, bbox_inches='tight')

def generate_scatter_plots(metrics, tools):
	fig = plt.figure(figsize=(8.5, 11.0))
	fig.suptitle(PLANNER_DOM[DOMAIN]+' '+PLANNER_DOM[PLANNER], fontsize=12)
	matplotlib.rcParams.update({'font.size': FONT_SIZE})
	matplotlib.rcParams.update({'font.family': FONT_FAMILY})
	matplotlib.rc('text', usetex=True)
	grid_ctr = 0
	for m_a, metric_x in enumerate(metrics):
		if metric_x not in ['Planning Results (%)']:
			for m_b, metric_y in enumerate(metrics):
				if metric_y not in ['Planning Results (%)']:
					if m_a != m_b:
						if m_a < m_b:
							ax = plt.subplot2grid((4,3), (m_a-1,m_b-2))
						else:
							ax = plt.subplot2grid((4,3), (m_a-1,m_b-1))
						for t in tools:
							plt.title(METRICS[metric_y]+' vs '+METRICS[metric_x], loc='center')
							samples_x	= metrics[metric_x]['sample']['Success (%)'][t]
							samples_y	= metrics[metric_y]['sample']['Success (%)'][t]
							plt.scatter(samples_x, samples_y, c=TOOLS[t]['color'], marker='.', linewidths=0)
							plt.xlabel(metric_x)
							plt.ylabel(metric_y)
							ax.set_xlim(left=0, right=None)
							ax.set_ylim(bottom=0, top=None)
							plt.legend([TOOLS[t]['tex'] for t in tools], loc='best', ncol=2, scatterpoints=1, fontsize=FONT_SIZE*0.75)
	plt.tight_layout()
	fig.subplots_adjust(top=0.94)
	for f in PLOT_FORMATS:
		plt.savefig(SCATTER_PLOT_NAME+DOMAIN+'_'+PLANNER+'.'+f, bbox_inches='tight')

def generate_box_plots(metrics, tools):
	fig = plt.figure(figsize=(8.0, 14.0))
	subplot_layout = (5,2)
	label_offset = (6,-6)
	fig.suptitle(PLANNER_DOM[DOMAIN]+' '+PLANNER_DOM[PLANNER], fontsize=12)
	matplotlib.rcParams.update({'font.size': FONT_SIZE})
	matplotlib.rcParams.update({'font.family': FONT_FAMILY})
	matplotlib.rc('text', usetex=True)
	for m, (metric_x, metric_y) in enumerate([('Makespan (s)', 'Number of Actions'),('Processing Time (s)', 'Memory Usage (GB)')]):

		# Data
		tcolors		= [TOOLS[t]['color'] for t in tools]
		tnames		= [TOOLS[t]['tex'] for t in tools]
		samples_x	= [metrics[metric_x]['sample']['Success (%)'][t] for t in tools]
		samples_y	= [metrics[metric_y]['sample']['Success (%)'][t] for t in tools]
		mean_x		= [stat.mean(s) for s in samples_x]
		mean_y		= [stat.mean(s) for s in samples_y]
		med_x		= [stat.median(s) for s in samples_x]
		med_y		= [stat.median(s) for s in samples_y]
		conf_x		= [1.96*stat.stdev(s)/(len(s)**0.5) for s in samples_x]
		conf_y		= [1.96*stat.stdev(s)/(len(s)**0.5) for s in samples_y]
		perc_x_l	= [np.percentile(s,25) for s in samples_x]
		perc_x_h	= [np.percentile(s,75) for s in samples_x]
		perc_y_l	= [np.percentile(s,25) for s in samples_y]
		perc_y_h	= [np.percentile(s,75) for s in samples_y]

		# Computing Pareto Domainance
		mean_dom = [sum([1 for tb in range(len(tools)) if mean_x[ta] < mean_x[tb] and mean_y[ta] < mean_y[tb]]) for ta in range(len(tools))]
		med_dom = [sum([1 for tb in range(len(tools)) if med_x[ta] < med_x[tb] and med_y[ta] < med_y[tb]]) for ta in range(len(tools))]

		def plot_details(title, loc='lower right'):
			plt.xlabel(metric_x)
			plt.ylabel(metric_y)
			plt.legend(tnames, loc=loc, ncol=2, scatterpoints=1, numpoints=1, fontsize=FONT_SIZE*0.75)
			plt.title(METRICS[metric_y]+' vs '+METRICS[metric_x]+': '+title, loc='center')

		# Mean and Confidence
		ax = plt.subplot2grid(subplot_layout, (0,m))
		for x, y, xerr, yerr, c in zip(mean_x, mean_y, conf_x, conf_y, tcolors):
			plt.errorbar(x=x, y=y, xerr=xerr, yerr=yerr, c=c)
		plot_details('Mean and Confidence')

		# Median and Quartiles
		ax = plt.subplot2grid(subplot_layout, (1,m))
		for x, y, xerr_l, xerr_h, yerr_l, yerr_h, c in zip(med_x, med_y, perc_x_l, perc_x_h, perc_y_l, perc_y_h, tcolors):
			plt.errorbar(x=x, y=y, xerr=[[xerr_l],[xerr_h]], yerr=[[yerr_l],[yerr_h]], c=c)
		plot_details('Median and Quartiles', loc='upper right')

		# Mean Pareto Dominance
		ax = plt.subplot2grid(subplot_layout, (2,m))
		for x, y, c, d in zip(mean_x, mean_y, tcolors, mean_dom):
			plt.plot(x, y, 's', c=c)
			plt.annotate(d, (x,y), xytext=label_offset, textcoords='offset points')
		plot_details('Mean Pareto Dominance')

		# Median Pareto Dominance
		ax = plt.subplot2grid(subplot_layout, (3,m))
		for x, y, c, d in zip(med_x, med_y, tcolors, med_dom):
			plt.plot(x, y, 'o', c=c)
			plt.annotate(d, (x,y), xytext=label_offset, textcoords='offset points')
		plot_details('Median Pareto Dominance')

		# Mean and Median
		ax = plt.subplot2grid(subplot_layout, (4,m))
		for xa, xb, ya, yb, c in zip(mean_x, med_x, mean_y, med_y, tcolors):
			plt.plot([xa,xb], [ya,yb], '-', c=c)
		for x, y, c in zip(mean_x, mean_y, tcolors):
			plt.plot(x, y, '-s', c=c)
		for x, y, c in zip(med_x, med_y, tcolors):
			plt.plot(x, y, '-o', c=c)
		plot_details('Mean and Median')

	plt.tight_layout()
	fig.subplots_adjust(top=0.95)
	for f in PLOT_FORMATS:
		plt.savefig(BOX_PLOT_NAME+DOMAIN+'_'+PLANNER+'.'+f, bbox_inches='tight')

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
for metric in tqdm(METRICS_AB.keys()):
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

# buf = ''
# for tools_baseline in TOOLS_BASELINE:
# 	general_kruskal_table = generate_general_kruskal_table(compute_general_kruskal(metrics, set([tools_baseline]) | set(TOOLS_RP)))
# 	buf += tools_baseline + '\n' + table_to_string(general_kruskal_table,',')
# with open(CSV_PREFIX+'kruskal_'+DOMAIN+'_'+PLANNER+'.csv', 'wb') as file:
# 	file.write(buf)

# Pair-wise Kruskal Tables
# print 'Pair-wise Kruskal Table ...'
# for f in STATUSES:
# 	with open(CSV_PREFIX+PAIRWISE+'_'+DOMAIN+'_'+PLANNER+'_'+STATUSES[f]['short'].replace(' ','')+'.csv', 'wb') as file:
# 		pairwise_kruskal_table = generate_pairwise_kruskal_table(compute_pairwise_kruskal(metrics,f))
# 		file.write(table_to_string(pairwise_kruskal_table,','))

# # Stats Table
# print 'Stats Table ...'
# with open(STATS_TABLE+DOMAIN+'_'+PLANNER+'.csv', 'wb') as file:
# 	stats_table = generate_stats_table(metrics)
# 	print table_to_string(stats_table)
# 	file.write(table_to_string(stats_table,','))
# 	# print tabulate(stats_table, headers="firstrow", tablefmt="latex")

# Stats Plots
# print 'Stats Plots ...'
# generate_stats_plots(metrics)

# # Scatter Plots
# print 'Stats Scatter ...'
# generate_scatter_plots(metrics, TOOLS)

# Box Plots
print 'Box Plots ...'
generate_box_plots(metrics, TOOLS)
