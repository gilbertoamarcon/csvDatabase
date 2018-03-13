#!/usr/bin/python
import os
import sys
import getopt
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

HELP_MSG = 'main.py -p <planner> -d <domain>\nplanner choices:\n\ttfddownward\n\tcolin2\ndomain choices:\n\tblocks_world\n\tfirst_response'

domain = 'blocks_world'
planner = 'tfddownward'
try:
	opts, args = getopt.getopt(sys.argv[1:],'hp:d:',['planner=','domain='])
except getopt.GetoptError:
	print HELP_MSG
	sys.exit(2)
for opt, arg in opts:
	if opt in ('-h', '--help'):
		print HELP_MSG
		sys.exit()
	elif opt in ('-p', '--planner'):
		planner = arg
	elif opt in ('-d', '--domain'):
		domain = arg
print 'Domain: %s' % domain
print 'Planner: %s' % planner

PLOT_LABELS = {('blocks_world','tfddownward'): ('a','b'), ('blocks_world','colin2'): ('c','d'), ('first_response','colin2'): ('e','f')}

# SPREAD			= 'STDEV'
SPREAD				= 'CI'

STATUSES			= OrderedDict([
							('Success (%)',			OrderedDict([	('short', 'Success'),	('long', 'Success'),		('code', 0),	('color', (0.000, 0.447, 0.741))	])), # Blue
							('Nonexecutable (%)',	OrderedDict([	('short', 'Nonexec'),	('long', 'Nonexecutable'),	('code', 1),	('color', (0.850, 0.325, 0.098))	])), # Tomato
							('Time Fail (%)',		OrderedDict([	('short', 'Time Fail'),	('long', 'Time Fail'),		('code', 124),	('color', (0.929, 0.694, 0.125))	])), # Orange
							('Memory Fail (%)',		OrderedDict([	('short', 'Mem Fail'),	('long', 'Memory Fail'),	('code', 134),	('color', (0.929, 0.894, 0.325))	])), # Yellow
					])

TOOLS	= OrderedDict([
			(('Object',25),					OrderedDict([	('reg', 'O25'),		('tex',r'\textbf{Object (0.25)}'),				('color', (1.000, 0.000, 0.000)), ('marker', (3,0,0))	])), # Red
			(('Object',50),					OrderedDict([	('reg', 'O50'),		('tex',r'\textbf{Object (0.50)}'),				('color', (1.000, 0.000, 0.000)), ('marker', (3,0,0))	])), # Red
			(('Action',25),					OrderedDict([	('reg', 'A25'),		('tex',r'\textbf{Action (0.25)}'),				('color', (0.000, 0.500, 0.000)), ('marker', (4,0,0))	])), # Green
			(('Action',50),					OrderedDict([	('reg', 'A50'),		('tex',r'\textbf{Action (0.50)}'),				('color', (0.000, 0.500, 0.000)), ('marker', (4,0,0))	])), # Green
			(('ActionObject',25),			OrderedDict([	('reg', 'AO25'),	('tex',r'\textbf{Action Object (0.25)}'),		('color', (0.000, 0.000, 1.000)), ('marker', (5,0,0))	])), # Blue
			(('ActionObject',50),			OrderedDict([	('reg', 'AO50'),	('tex',r'\textbf{Action Object (0.50)}'),		('color', (0.000, 0.000, 1.000)), ('marker', (5,0,0))	])), # Blue
			(('ObjectTime',25),				OrderedDict([	('reg', 'OT25'),	('tex',r'\textbf{Object Time (0.25)}'),			('color', (1.000, 0.500, 0.500)), ('marker', (3,0,180))	])), # Pink
			(('ObjectTime',50),				OrderedDict([	('reg', 'OT50'),	('tex',r'\textbf{Object Time (0.50)}'),			('color', (1.000, 0.500, 0.500)), ('marker', (3,0,180))	])), # Pink
			(('ActionTime',25),				OrderedDict([	('reg', 'AT25'),	('tex',r'\textbf{Action Time (0.25)}'),			('color', (0.500, 1.000, 0.500)), ('marker', (4,0,45))	])), # Light Green
			(('ActionTime',50),				OrderedDict([	('reg', 'AT50'),	('tex',r'\textbf{Action Time (0.50)}'),			('color', (0.500, 1.000, 0.500)), ('marker', (4,0,45))	])), # Light Green
			(('ActionObjectTime',25),		OrderedDict([	('reg', 'AOT25'),	('tex',r'\textbf{Action Object Time (0.25)}'),	('color', (0.000, 0.750, 1.000)), ('marker', (5,0,180))	])), # Light Blue
			(('ActionObjectTime',50),		OrderedDict([	('reg', 'AOT50'),	('tex',r'\textbf{Action Object Time (0.50)}'),	('color', (0.000, 0.750, 1.000)), ('marker', (5,0,180))	])), # Light Blue
			(('CoalitionSimilarity',25),	OrderedDict([	('reg', 'CS25'),	('tex','Coalition Similarity (0.25)'),			('color', (0.500, 0.000, 0.500)), ('marker', (6,0,0))	])), # Purple
			(('CoalitionSimilarity',50),	OrderedDict([	('reg', 'CS50'),	('tex','Coalition Similarity (0.50)'),			('color', (0.500, 0.000, 0.500)), ('marker', (6,0,0))	])), # Purple
			(('CoalitionAssistance',25),	OrderedDict([	('reg', 'CA25'),	('tex','Coalition Assistance (0.25)'),			('color', (1.000, 0.500, 1.000)), ('marker', (6,0,30))	])), # Light Purple
			(('CoalitionAssistance',50),	OrderedDict([	('reg', 'CA50'),	('tex','Coalition Assistance (0.50)'),			('color', (1.000, 0.500, 1.000)), ('marker', (6,0,30))	])), # Light Purple
			(('CFP',0),						OrderedDict([	('reg', 'CFP'),		('tex','Coalition Formation and Planning'),		('color', (0.000, 0.000, 0.000)), ('marker', (7,0,0))	])), # Black
			(('PA',0),						OrderedDict([	('reg', 'PA'),		('tex','Planning Alone'),						('color', (0.500, 0.500, 0.500)), ('marker', (7,0,180))	])), # Grey
		])

if domain == 'first_response':
	del TOOLS[('PA',0)]

METRICS				= OrderedDict([
							('Planning Results (%)',	{'ab': 'a) Planning results',	'plain': 'Planning results',	'excl': []}),
							('Makespan (s)',			{'ab': 'b) Makespan',			'plain': 'Makespan',			'excl': ['Nonexecutable (%)','Time Fail (%)','Memory Fail (%)']}),
							('Number of Actions',		{'ab': 'c) Number of actions',	'plain': 'Number of actions',	'excl': ['Nonexecutable (%)','Time Fail (%)','Memory Fail (%)']}),
							('Processing Time (s)',		{'ab': 'd) Processing time',	'plain': 'Processing time',		'excl': ['Time Fail (%)']}),
							('Memory Usage (GB)',		{'ab': 'e) Memory usage',		'plain': 'Memory usage',		'excl': ['Memory Fail (%)']}),
					])

PLANNER_DOM			= {'first_response': 'First Response', 'blocks_world': 'Blocks World', 'colin2': 'COLIN', 'tfddownward': 'TFD'}

# Labels
file_header			= ['Domain','Problem','CFA','Planner','Tool','Fusion Ratio', 'Planning Results (%)', 'Makespan (s)', 'Number of Actions', 'Processing Time (s)', 'Memory Usage (GB)']

BAR_FILL			= 0.60
FONT_SIZE			= 7
FONT_FAMILY			= 'serif'
COL_PAD				= 5
CSPACING			= 1

# File names
GATHER_DATA_SCRIPT	= 'scripts/gather_data.sh'
RAW_STATS			= 'csv/stats.csv'
FILTERED_STATS		= 'csv/stats_filtered.csv'
STATS_TABLE			= 'tex/stats_'
PLOT_FORMATS		= ['pdf', 'eps', 'svg']
STATS_PLOT_NAME		= 'plots/stats_'
BOX_PLOT_NAME		= 'plots/box_'

NCOL				= 4

MARKER_SIZE			= 5
TICK_SIZE			= 2
LINE_WIDTH			= 0.50
FIG_SIZE			= (12.0, 8.0)
LABEL_OSET_RESULTS	= 0.50
LABEL_OSET_METRICS	= -0.6


def generate_stats_table(metrics):
	ret_var = []
	for metric in metrics:
		buff = [['']+[STATUSES[f]['long'] for f in STATUSES if f not in METRICS[metric]['excl']]]
		for t in TOOLS.keys():
			trow = [TOOLS[t]['tex']]
			for f in [f for f in STATUSES if f not in METRICS[metric]['excl']]:
				if metric == 'Planning Results (%)':
					trow.append('%d'%metrics[metric][f][t])
				else:
					mean	= metrics[metric]['mean'][f][t]
					error	= metrics[metric]['error'][f][t]
					trow.append('%.*f (%.*f)'%(CSPACING,mean,CSPACING,error) if mean == mean and error ==  error else 'N/A')
			buff.append(trow)
		ret_var.append(tabulate(buff, headers='firstrow', tablefmt='latex_raw'))
	return '\n'.join(ret_var)


def generate_stats_plots(metrics):
	plt.figure(figsize=FIG_SIZE)
	matplotlib.rcParams.update({'font.size': FONT_SIZE})
	matplotlib.rcParams.update({'font.family': FONT_FAMILY})
	matplotlib.rcParams.update({'axes.linewidth': LINE_WIDTH})
	matplotlib.rcParams.update({'xtick.major.width': LINE_WIDTH})
	matplotlib.rcParams.update({'ytick.major.width': LINE_WIDTH})
	matplotlib.rcParams.update({'xtick.major.size': TICK_SIZE})
	matplotlib.rcParams.update({'ytick.major.size': TICK_SIZE})
	matplotlib.rc('text', usetex=True)
	gridspec.GridSpec(9,1)
	numbars = len(TOOLS)
	bar_origin = ((1-BAR_FILL)/2)*np.ones(numbars) + np.asarray(range(numbars))

	# For each metric
	grid_ctr = 0
	for m, metric in enumerate(metrics):
		if metric == 'Planning Results (%)':

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

			# plt.title(METRICS[metric]['plain']+' for each tool.', loc='left')
			ax.xaxis.grid(True, which='major', color='grey', linestyle='-')
			ax.set_axisbelow(True)

			shift_pos = bar_origin
			if metric == 'Planning Results (%)':
				label_succ = []
				for f in STATUSES:
					label_succ.append(STATUSES[f]['long'])
				barl = np.array([100.00]*len(TOOLS))
				bar_handle = []
				for i,f in enumerate(list(reversed(STATUSES.keys()))):
					bar_handle.append(plt.barh(shift_pos, barl, bar_width, color=STATUSES[f]['color'], linewidth=LINE_WIDTH))
					barl -= np.array(list(reversed(metrics[metric][f].values())))
				legend = plt.legend(list(reversed(bar_handle)), label_succ, loc='lower center', bbox_to_anchor=(LABEL_OSET_RESULTS,1.0), ncol=NCOL, fontsize=FONT_SIZE*0.87)
				legend.get_frame().set_linewidth(LINE_WIDTH)
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
						plt.barh(shift_pos+bar_width*counter, means, bar_width, color=STATUSES[f]['color'], linewidth=LINE_WIDTH, xerr=errors, ecolor='k')
						counter -= 1
				else:
					means	= list(reversed(metrics[metric]['mean']['Success (%)'].values()))
					errors	= list(reversed(metrics[metric]['error']['Success (%)'].values()))
					plt.barh(shift_pos+bar_width*0, means, bar_width, color=STATUSES['Success (%)']['color'], linewidth=LINE_WIDTH, xerr=errors, ecolor='k')
			ax.set_xlim(left=0, right=None)

			plt.xlabel(metric.replace('%','\%'))
			plt.yticks(bar_origin+BAR_FILL/2, list(reversed([k['tex'] for k in TOOLS.values()])))
			plt.ylim([0, numbars]) 

		# Legend and ticks
		plt.tight_layout()
		for f in PLOT_FORMATS:
			plt.savefig(STATS_PLOT_NAME+domain+'_'+planner+'.'+f, bbox_inches='tight')

def generate_box_plots(metrics, tools):
	fig = plt.figure(figsize=(6.0, 2.00))
	subplot_layout = (1,2)
	label_offset = (4,-4)
	matplotlib.rcParams.update({'font.size': FONT_SIZE})
	matplotlib.rcParams.update({'font.family': FONT_FAMILY})
	matplotlib.rcParams.update({'axes.linewidth': LINE_WIDTH})
	matplotlib.rcParams.update({'xtick.major.width': LINE_WIDTH})
	matplotlib.rcParams.update({'ytick.major.width': LINE_WIDTH})
	matplotlib.rcParams.update({'xtick.major.size': TICK_SIZE})
	matplotlib.rcParams.update({'ytick.major.size': TICK_SIZE})
	matplotlib.rc('text', usetex=True)
	titles = ['Quality', 'Cost']
	for m, (metric_x, metric_y) in enumerate([('Makespan (s)', 'Number of Actions'),('Processing Time (s)', 'Memory Usage (GB)')]):

		# Data
		tcolors		= [TOOLS[t]['color'] for t in tools]
		tmarkers	= [TOOLS[t]['marker'] for t in tools]
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

		def plot_details():
			plt.xlabel(metric_x)
			plt.ylabel(metric_y)
			if m == 0 and planner in ['tfddownward']:
				legend = plt.legend(tnames, loc='lower center', ncol=10, scatterpoints=1, numpoints=1, fontsize=FONT_SIZE*0.915, bbox_to_anchor=(1.07,1.0))
				legend.get_frame().set_linewidth(LINE_WIDTH)
			ax.text(0.0, -0.35,PLOT_LABELS[(domain,planner)][m]+') '+PLANNER_DOM[domain]+' '+titles[m]+' Objectives ('+PLANNER_DOM[planner]+')', verticalalignment='bottom', horizontalalignment='left', transform=ax.transAxes, fontsize=FONT_SIZE)

		# Mean Pareto Dominance
		ax = plt.subplot2grid(subplot_layout, (0,m))
		limits_x = [min(mean_x), max(mean_x)]
		limits_y = [min(mean_y), max(mean_y)]
		margin_x = (limits_x[1] - limits_x[0])*0.1
		margin_y = (limits_y[1] - limits_y[0])*0.1
		limits_x= [limits_x[0] - margin_x, limits_x[1] + margin_x]
		limits_y= [limits_y[0] - margin_y, limits_y[1] + margin_y]
		for x, y, c, mkr, d in zip(mean_x, mean_y, tcolors, tmarkers, mean_dom):
			# plt.annotate(d, (x,y), xytext=label_offset, textcoords='offset points', fontsize=0.75*FONT_SIZE,arrowprops=dict(edgecolor='none',facecolor='grey', width=0.0, headwidth=LINE_WIDTH, shrink=0.50))
			plt.annotate(d, (x,y), xytext=label_offset, textcoords='offset points', fontsize=FONT_SIZE)
			plt.plot(x, y, ls='None', marker=mkr, c=c, ms=MARKER_SIZE, mew=0.1*MARKER_SIZE)
		ax.set_xlim(limits_x)
		ax.set_ylim(limits_y)
		plot_details()

	plt.tight_layout()
	fig.subplots_adjust(top=0.85)
	for f in PLOT_FORMATS:
		plt.savefig(BOX_PLOT_NAME+domain+'_'+planner+'.'+f, bbox_inches='tight')

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
		if metric == 'Planning Results (%)':
			query_all	= db.query([('Domain',domain),('Planner',planner),('Tool',t[0]),('Fusion Ratio','0.%02d'%t[1])])
			status		= db.select('Planning Results (%)', query_all, as_integer=True)
			for f in STATUSES:
				metrics[metric][f][t] = 100.0*len([k for k in status if k == STATUSES[f]['code']])/len(query_all)
		else:
			for f in STATUSES:
				sample = db.select(metric, db.query([('Domain',domain),('Planner',planner),('Tool',t[0]),('Fusion Ratio','0.%02d'%t[1]),('Planning Results (%)',str(STATUSES[f]['code']))]), as_float=True)
				mean, error = get_stats(sample)
				metrics[metric]['mean'][f][t]	= mean
				metrics[metric]['error'][f][t]	= error
				metrics[metric]['sample'][f][t]	= sample

# Stats Table
print 'Stats Table ...'
with open(STATS_TABLE+domain+'_'+planner+'.tex', 'wb') as file:
	file.write(generate_stats_table(metrics))

# Stats Plots
print 'Stats Plots ...'
generate_stats_plots(metrics)

# # Box Plots
# print 'Box Plots ...'
# generate_box_plots(metrics, TOOLS)
