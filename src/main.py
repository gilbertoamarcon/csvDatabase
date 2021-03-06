#!/usr/bin/python
import os
import sys
import getopt
import matplotlib
import math
import operator
import re
import matplotlib.pyplot as plt
import pytablewriter as ptw
import numpy as np
import pandas as pd
from tqdm import tqdm
from tabulate import tabulate
from collections import OrderedDict
import matplotlib.gridspec as gridspec
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

# PLOT_LABELS = {('blocks_world','tfddownward'): ('a','b'), ('blocks_world','colin2'): ('c','d'), ('first_response','colin2'): ('e','f')}

SPREAD			= 'STDEV'
# SPREAD				= 'CI'


COLOR_SCHEME = {
	 0: {'color': (0.000, 1.000, 0.000), 'rank': 'Best'},
	 1: {'color': (1.000, 1.000, 0.000), 'rank': 'Second Best'},
	 2: {'color': (1.000, 0.750, 0.000), 'rank': 'Third Best'},
	 3: {'color': (1.000, 1.000, 1.000), 'rank': 'Fourth Best'},
	-1: {'color': (1.000, 0.000, 0.000), 'rank': 'Worst'},
}

FOURTH_BEST = [
	('blocks_world','tfddownward',0),
	('blocks_world','colin2',1),
]


STATUSES	= OrderedDict([
			('Success (%)',			OrderedDict([	('name', 'Success'),		('acro', 'Success'),	('code',   0),	('color', (0.000, 0.447, 0.741))	])), # Blue
			('Nonexecutable (%)',	OrderedDict([	('name', 'Nonexecutable'),	('acro', 'Nonexec'),	('code',   1),	('color', (0.850, 0.325, 0.098))	])), # Tomato
			('Time Fail (%)',		OrderedDict([	('name', 'Time Fail'),		('acro', 'Time Fail'),	('code', 124),	('color', (0.929, 0.694, 0.125))	])), # Orange
			('Memory Fail (%)',		OrderedDict([	('name', 'Memory Fail'),	('acro', 'Mem Fail'),	('code', 134),	('color', (0.929, 0.894, 0.325))	])), # Yellow
		])

TOOL_FORMAT	= OrderedDict([
			('Object',				OrderedDict([	('name','Object'),								('acro','O'),	('color', (1.00, 0.00, 0.00)),	('marker', (3,0,  0)),	('bold', True)])),
			('Action',				OrderedDict([	('name','Action'),								('acro','A'),	('color', (0.00, 0.50, 0.00)),	('marker', (4,0,  0)),	('bold', True)])),
			('ActionObject',		OrderedDict([	('name','Action-Object'),						('acro','AO'),	('color', (0.00, 0.00, 1.00)),	('marker', (5,0,  0)),	('bold', True)])),
			('ObjectTime',			OrderedDict([	('name','Object-Temporal'),						('acro','OT'),	('color', (1.00, 0.50, 0.50)),	('marker', (3,0,180)),	('bold', True)])),
			('ActionTime',			OrderedDict([	('name','Action-Temporal'),						('acro','AT'),	('color', (0.50, 1.00, 0.50)),	('marker', (4,0, 45)),	('bold', True)])),
			('ActionObjectTime',	OrderedDict([	('name','Action-Object-Temporal'),				('acro','AOT'),	('color', (0.00, 0.75, 1.00)),	('marker', (5,0,180)),	('bold', True)])),
			('CoalitionSimilarity',	OrderedDict([	('name','Coalition Similarity'),				('acro','CS'),	('color', (0.50, 0.00, 0.50)),	('marker', (6,0,  0)),	('bold', False)])),
			('CoalitionAssistance',	OrderedDict([	('name','Coalition Assistance'),				('acro','CA'),	('color', (1.00, 0.50, 1.00)),	('marker', (6,0, 30)),	('bold', False)])),
			('CFP',					OrderedDict([	('name','Coalition Formation and Planning'),	('acro','CFP'),	('color', (0.00, 0.00, 0.00)),	('marker', (7,0,  0)),	('bold', False)])),
			('PA',					OrderedDict([	('name','Planning Alone'),						('acro','PA'),	('color', (0.50, 0.50, 0.50)),	('marker', (7,0,180)),	('bold', False)])),
		])

TIME_ORDER = ['Object','Action','ActionObject','CoalitionSimilarity','ObjectTime','ActionTime','ActionObjectTime','CoalitionAssistance']

TF_TOOLS_RAW = ['Object','Action','ActionObject','ObjectTime','ActionTime','ActionObjectTime','CoalitionSimilarity','CoalitionAssistance']
BASES = ['CFP','PA']

FRS = [0.25,0.50,0.75,1.00]

TF_TOOLS = [(t,d) for t in TF_TOOLS_RAW for d in FRS]
TOOLS	= TF_TOOLS + [(t,0) for t in BASES]

METRICS	= OrderedDict([
			('Planning Results (%)',	{'ac': 'Planning results (\%)',	'ab': 'a) Planning results',	'plain': 'Planning results',	'flat': 'planning_results',		'excl': []}),
			('Makespan (s)',			{'ac': 'Makespan (s)',			'ab': 'b) Makespan',			'plain': 'Makespan',			'flat': 'makespan',				'excl': ['Nonexecutable (%)','Time Fail (%)','Memory Fail (%)']}),
			('Number of Actions',		{'ac': 'Number of actions',		'ab': 'c) Number of actions',	'plain': 'Number of actions',	'flat': 'number_of_actions',	'excl': ['Nonexecutable (%)','Time Fail (%)','Memory Fail (%)']}),
			('Processing Time (s)',		{'ac': 'Processing time (m)',	'ab': 'd) Processing time',		'plain': 'Processing time',		'flat': 'processing_time',		'excl': ['Time Fail (%)']}),
			('Memory Usage (GB)',		{'ac': 'Memory usage (GB)',		'ab': 'e) Memory usage',		'plain': 'Memory usage',		'flat': 'memory_usage',			'excl': ['Memory Fail (%)']}),
		])

PLANNER_DOM			= {'first_response': 'First Response', 'blocks_world': 'Blocks World', 'colin2': 'COLIN', 'tfddownward': 'TFD'}

# Labels
file_header			= ['Domain','Problem','CFA','Planner','Tool','Fusion Ratio', 'Planning Results (%)', 'Makespan (s)', 'Number of Actions', 'Processing Time (s)', 'Memory Usage (GB)']

BAR_FILL			= 0.60
FONT_SIZE			= 6
FONT_FAMILY			= 'serif'
COL_PAD				= 5
CSPACING			= 0
DECPRES				= 1

SORT_SUCCESS		= True
MINUTES				= True

# File names
GATHER_DATA_SCRIPT	= 'scripts/gather_data.sh'
RAW_STATS			= 'csv/stats.csv'
FILTERED_STATS		= 'csv/stats_filtered.csv'
STATS_TABLE			= 'tex/stats_'
FMAX_TABLE			= 'tex/fmax_'
EXCEL_TABLE			= 'xls/stats'
EXCEL_FMAX			= 'xls/fmax'
PLOT_FORMATS		= ['pdf', 'eps', 'svg']
FMAX_PLOTS			= 'plots/fmax_'
STATS_PLOT_NAME		= 'plots/stats_'
BOX_PLOT_NAME		= 'plots/box_'
BOX_SINGLE_FIG_NAME	= 'plots/box_single_'
BOX_MARGIN			= 0.2
BOX_TABLE_ROW_SIZE	= 0.07

NCOL				= 4

MARKER_SIZE			= 3
TICK_SIZE			= 2
LINE_WIDTH			= 0.50
STATS_FIG_SIZE		= {
	'blocks_world': {
		'tfddownward': (9.0,11.6),
		'colin2': (9.0,12.5),
	},
	'first_response': {
		'colin2': (9.0,11.9),
	},
}
FMAX_FIG_SIZE		= (4.5,3.0)
BOX_SINGLE_FIG_SIZE	= (4.5,4.5)
BOX_FIG_SIZE		= {
	'blocks_world': {
		# 'tfddownward': (4.5,6.3),
		'tfddownward': (4.3,2.05),
		'colin2': (4.3,1.95),
	},
	'first_response': {
		'colin2': (4.3,2.05),
	},
}

BOX_LABEL_OFFSET	= (5,-5)
LABEL_OSET_RESULTS	= 0.50
LABEL_OSET_METRICS	= -0.6
PAD_INCHES			= 0.025

if domain == 'first_response':
	TOOLS.remove(('PA',0))

def format_tool_name(type, key):

	# Tool name and acronym
	name = TOOL_FORMAT[key[0]]['name']
	acro = TOOL_FORMAT[key[0]]['acro']

	# Bold
	if TOOL_FORMAT[key[0]]['bold']:
		name = '\\textbf{%s}'%name
		acro = '\\textbf{%s}'%acro

	# Format
	if type == 'fusion-ratio':
		return 'N/A' if key[1]==0.0 else '$%4.2f$'%key[1]
	if type == 'name':
		return name + ('' if key[1]==0.0 else r' ($f_{max} = ' + '%4.2f'%key[1] + r'$)')
	if type == 'acro':
		return acro
	if type == 'table-name':
		if key[1]==0.00:
			return name
		if key[1]==0.25:
			return r'\multirow{&}{*}{%s}'%name
		if key[1]==0.50:
			return ''
		if key[1]==0.75:
			return ''
		if key[1]==1.00:
			return ''

def generate_excel(filename,metrics):
	print 'Storing data to %s ...' % filename
	writer = ptw.ExcelXlsxTableWriter()
	writer.open(filename)
	for metric in metrics:
		writer.make_worksheet(METRICS[metric]['plain'].replace(' ','_'))
		header = ['Tool','f_max']+STATUSES.keys()
		data = [[t[0], format_tool_name('fusion-ratio',t)] + ['%d'%metrics[metric][f][t] if metric == 'Planning Results (%)' else '%*.*f'%(CSPACING,DECPRES,metrics[metric]['mean'][f][t]) for f in STATUSES] for t in TOOLS]
		writer.header_list = header
		writer.value_matrix = data
		writer.write_table()
	writer.close()



def generate_excel_fmax(filename,metrics):

	# Building dataframe
	frames = []
	for metric in metrics:
		data = OrderedDict([('%.2f'%t[1],[]) for t in TF_TOOLS])
		for t in TF_TOOLS:
			if metric == 'Planning Results (%)':
				entry = metrics[metric]['Success (%)'][t]
			else:
				entry = metrics[metric]['mean']['Success (%)'][t]
			data['%.2f'%t[1]].append(entry)
		frames.append(pd.DataFrame(data=data,index=[TOOL_FORMAT[t]['acro'] for t in TF_TOOLS_RAW]))
	df = pd.concat(frames, keys=metrics, axis=1)

	# To spreadsheet
	writer = pd.ExcelWriter(filename)
	df.to_excel(writer,'data')
	per_format = writer.book.add_format({'num_format': '0.'})
	num_format = writer.book.add_format({'num_format': '0.0'})
	writer.sheets['data'].set_column('A:E', 5, per_format)
	writer.sheets['data'].set_column('F:Z', 5, num_format)
	writer.save()


def generate_fmax_table(metrics):

	index = [(format_tool_name('acro',t),format_tool_name('fusion-ratio',t)) for t in TF_TOOLS]
	tname_acro = OrderedDict([(i[0],None) for i in index]).keys()

	# Pareto values
	pareto = OrderedDict()
	for (name,metric_x,metric_y) in [('Quality Pareto Strength','Makespan (s)', 'Number of Actions'),('Cost Pareto Strength','Processing Time (s)', 'Memory Usage (GB)')]:
		pareto[name] = compute_pareto_domainance(metrics, TF_TOOLS, metric_x, metric_y)

	df = pd.DataFrame(data=pareto,index=pd.MultiIndex.from_tuples(index,names=['',r'\textbf{Tool}']))
	df = df.unstack(level=[1],fill_value='').reindex(tname_acro)
	num_columns = len(pareto)*len(index)/len(tname_acro)
	ret_var = df.to_latex(
			bold_rows			= False,
			multirow			= True,
			escape				= False,
			multicolumn_format	= 'c',
		)

	# Removing horizontal lines
	for r in ['bottomrule','toprule']:
		ret_var = re.sub(r'\n*\\'+r,'',ret_var)

	# Removing empty lines
	ret_var = re.sub(r'\n[\s\&\\]*\n','\n',ret_var)

	# Short horizontal lines
	re_key = r'\n*\\midrule'
	reg_sub = r' \\Cline{1pt}{1-%d}' % (num_columns+1)
	ret_var = re.sub(re_key,reg_sub,ret_var)

	# Thick vline
	re_key = r'(\{[lcr]{'+str(num_columns+1)+r'}\})'
	rs = r'|'.join(['r']*(len(index)/len(tname_acro)))
	reg_sub = r'{c'+''.join(len(pareto)*[' V{3} %s'%rs])+'}'
	ret_var = re.sub(re_key,reg_sub,ret_var)

	# Long horizontal lines
	re_key = r'(\\\\)(\n\s*[^&\s]+[^&]*&)'
	reg_sub = r'\1 \\hline\2'
	ret_var = re.sub(re_key,reg_sub,ret_var)

	return ret_var

def generate_stats_table(metrics,metric):
	ret_var = []
	buff = [[r'\textbf{Tool}','$f_{max}$']+[r'\textbf{'+STATUSES[f]['name']+'}' for f in STATUSES if f not in METRICS[metric]['excl']]]
	columns = [f for f in STATUSES if f not in METRICS[metric]['excl'] and not np.isnan(metrics[metric]['mean'][f].values()).all()]
	for t in TOOLS:
		trow = [format_tool_name('table-name',t), format_tool_name('fusion-ratio',t)]
		for f in columns:
			if metric == 'Planning Results (%)':
				trow.append('%d'%metrics[metric][f][t])
			else:
				mean	= metrics[metric]['mean'][f][t]
				error	= metrics[metric]['error'][f][t]
				trow.append('%*.*f (%*.*f)'%(CSPACING,DECPRES,mean,CSPACING,DECPRES,error) if mean == mean and error ==  error else 'N/A')
		buff.append(trow)
	ret_var.append(tabulate(buff, headers='firstrow', tablefmt='latex_raw'))

	ret_var = '\n'.join(ret_var)

	num_columns = len(columns)

	# Multirows
	re_key = r'\\multirow{&}'
	reg_sub = r'\\multirow{%d}'%(num_columns+1)
	ret_var = re.sub(re_key,reg_sub,ret_var)

	# Removing horizontal lines
	re_key = r'\n*\\hline'
	reg_sub = r''
	ret_var = re.sub(re_key,reg_sub,ret_var)

	# Long horizontal lines
	re_key = r'(\\\\)(\n\s*[^&\s]+[^&]*&)'
	reg_sub = r'\1 \\hline\2'
	ret_var = re.sub(re_key,reg_sub,ret_var)

	# Short horizontal lines
	re_key = r'(\\\\)(\n\s*&)'
	reg_sub = r'\1 \\Cline{0.5pt}{2-%d}\2' % (num_columns+2)
	ret_var = re.sub(re_key,reg_sub,ret_var)

	# Thick vline
	re_key = r'(\{l+\})'
	rs = r'|'.join(['r']*num_columns)
	reg_sub = r'{l|c V{3} %s}'%rs
	ret_var = re.sub(re_key,reg_sub,ret_var)

	# Thick main horizontal line
	re_key = r'((?!\hline)*)\hline([\S\s]*)'
	reg_sub = r'\1Cline{1pt}{1-%d}\2' % (num_columns+2)
	ret_var = re.sub(re_key,reg_sub,ret_var)

	return ret_var


def set_fig_text_format():
	matplotlib.rcParams.update({'font.size': 			FONT_SIZE})
	matplotlib.rcParams.update({'font.family':			FONT_FAMILY})
	matplotlib.rcParams.update({'axes.linewidth':		LINE_WIDTH})
	matplotlib.rcParams.update({'xtick.major.width':	LINE_WIDTH})
	matplotlib.rcParams.update({'ytick.major.width':	LINE_WIDTH})
	matplotlib.rcParams.update({'xtick.major.size':		TICK_SIZE})
	matplotlib.rcParams.update({'ytick.major.size':		TICK_SIZE})
	matplotlib.rc('text', usetex=True)

def generate_stats_plots(metrics):
	plt.figure(figsize=STATS_FIG_SIZE[domain][planner])
	set_fig_text_format()
	gridspec.GridSpec(9,1)
	numbars = len(TOOLS)
	bar_origin = ((1-BAR_FILL)/2)*np.ones(numbars) + np.asarray(range(numbars))

	# For each metric
	grid_ctr = 0
	for m, metric in enumerate(metrics):
		if metric == 'Planning Results (%)':

			# Sorting for success
			if SORT_SUCCESS:
				sorted_keys = list(reversed([k[0] for k in sorted(metrics[metric]['Success (%)'].items(), key=operator.itemgetter(1))]))
			else:
				sorted_keys = metrics[metric]['Success (%)'].keys()


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
					label_succ.append(STATUSES[f]['acro'])
				barl = np.array([100.00]*len(TOOLS))
				bar_handle = []
				for i,f in enumerate(list(reversed(STATUSES.keys()))):
					bar_handle.append(plt.barh(shift_pos, barl, bar_width, color=STATUSES[f]['color'], linewidth=LINE_WIDTH))
					# barl -= np.array(list(reversed(metrics[metric][f].values())))
					barl -= np.array(list(reversed([metrics[metric][f][k] for k in sorted_keys])))
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
			# plt.yticks(bar_origin+BAR_FILL/2, list(reversed([k['name'] for k in TOOLS.values()])))
			plt.yticks(bar_origin+BAR_FILL/2, list(reversed([format_tool_name('name',k) for k in sorted_keys])))
			plt.ylim([0, numbars]) 

		# Legend and ticks
		plt.tight_layout()
		for f in PLOT_FORMATS:
			plt.savefig(STATS_PLOT_NAME+domain+'_'+planner+'.'+f, bbox_inches='tight', pad_inches=PAD_INCHES)

def generate_fmax_plots(metrics):

	# Time order Sorting
	time_order = True
	FMAX_TF_TOOLS = [(t,d) for t in TIME_ORDER for d in FRS] if time_order else TF_TOOLS

	tcolors	= [TOOL_FORMAT[t[0]]['color'] for t in FMAX_TF_TOOLS][::4]
	markers	= [TOOL_FORMAT[t[0]]['marker'] for t in FMAX_TF_TOOLS][::4]
	tnames	= [format_tool_name('acro',t) for t in FMAX_TF_TOOLS][::4]

	plt.figure(figsize=FMAX_FIG_SIZE)
	set_fig_text_format()
	for n,metric in enumerate(metrics):

		data = OrderedDict([(t[0],[]) for t in FMAX_TF_TOOLS])
		for t in FMAX_TF_TOOLS:
			data[t[0]].append(metrics[metric]['Success (%)'][t] if metric == 'Planning Results (%)' else metrics[metric]['mean']['Success (%)'][t])
		lists = [d for d in data.values()]

		frame_x = int(math.floor((n+0)/3))
		frame_y = (n+0)%3

		ax = plt.subplot2grid((2,3), (frame_x,frame_y))
		for t in range(len(lists)):
			ax = plt.plot(FRS, lists[t], c=tcolors[t], marker=markers[t], ms=MARKER_SIZE)

		# Legend
		if n == 2:
			# legend = plt.legend(tnames, loc='center', ncol=2, scatterpoints=1, numpoints=1, fontsize=FONT_SIZE, bbox_to_anchor=(-0.75,0.5))
			legend = plt.legend(tnames, loc='center', ncol=2, scatterpoints=1, numpoints=1, fontsize=FONT_SIZE, bbox_to_anchor=(0.5,-1.0))
			legend.get_frame().set_linewidth(LINE_WIDTH)

		# Labels and ticks
		plt.xticks(FRS)
		extrap = 0.05
		plt.xlim(min(FRS)-extrap,max(FRS)+extrap)
		xlabel_name = 'a) Success (%)'.replace('%','\%')
		ylabel_name = 'Success (%)'.replace('%','\%')
		if metric != 'Planning Results (%)':
			xlabel_name = METRICS[metric]['ab']
			ylabel_name = METRICS[metric]['ac']
		plt.xlabel('Fusion Ratio ($f_{max}$)\n'+xlabel_name,linespacing=2.0)
		plt.ylabel(ylabel_name)

	plt.tight_layout()
	for f in PLOT_FORMATS:
		plt.savefig(FMAX_PLOTS+domain+'_'+planner+'.'+f, bbox_inches='tight', pad_inches=PAD_INCHES)

def compute_box_limits(metrics, tools, metric_x, metric_y):
	mean_x		= [np.mean(metrics[metric_x]['sample']['Success (%)'][t]) for t in tools]
	mean_y		= [np.mean(metrics[metric_y]['sample']['Success (%)'][t]) for t in tools]
	limits_x = [min(mean_x), max(mean_x)]
	limits_y = [min(mean_y), max(mean_y)]
	margin_x = (limits_x[1] - limits_x[0])*0.1
	margin_y = (limits_y[1] - limits_y[0])*0.1
	limits_x = [limits_x[0] - margin_x, limits_x[1] + margin_x]
	limits_y = [limits_y[0] - margin_y, limits_y[1] + margin_y]
	return limits_x,limits_y

def compute_pareto_domainance(metrics, tools, metric_x, metric_y):
	mean_x		= {t:np.mean(metrics[metric_x]['sample']['Success (%)'][t]) for t in TOOLS}
	mean_y		= {t:np.mean(metrics[metric_y]['sample']['Success (%)'][t]) for t in TOOLS}
	return [sum([1 for tb in TOOLS if mean_x[ta] < mean_x[tb] and mean_y[ta] < mean_y[tb]]) for ta in tools]

def generate_box_plots(metrics):
	fig = plt.figure(figsize=BOX_FIG_SIZE[domain][planner])
	subplot_layout = (len(FRS),2)
	label_offset = BOX_LABEL_OFFSET
	set_fig_text_format()
	titles = ['Quality', 'Cost']
	for fr,tools in enumerate([[k for k in TOOLS if k[1] in [tx,0]] for tx in FRS]):
		for m, (metric_x, metric_y) in enumerate([('Makespan (s)', 'Number of Actions'),('Processing Time (s)', 'Memory Usage (GB)')]):

			# Data
			tcolors	= [TOOL_FORMAT[t[0]]['color'] for t in tools]
			markers	= [TOOL_FORMAT[t[0]]['marker'] for t in tools]
			tnames	= [format_tool_name('acro',t) for t in tools]
			mean_x	= [np.mean(metrics[metric_x]['sample']['Success (%)'][t]) for t in tools]
			mean_y	= [np.mean(metrics[metric_y]['sample']['Success (%)'][t]) for t in tools]

			# Computing Pareto Domainance
			mean_dom = compute_pareto_domainance(metrics, tools, metric_x, metric_y)

			# Mean Pareto Dominance
			ax = plt.subplot2grid(subplot_layout, (fr,m))
			for x, y, c, mkr, d in zip(mean_x, mean_y, tcolors, markers, mean_dom):
				plt.annotate(d, (x,y), xytext=label_offset, textcoords='offset points', fontsize=0.75*FONT_SIZE)
				plt.plot(x, y, ls='None', c=c, marker=mkr, ms=MARKER_SIZE)

			# Plot limits
			limits_x,limits_y = compute_box_limits(metrics, TOOLS, metric_x, metric_y)
			ax.set_xlim(limits_x)
			ax.set_ylim(limits_y)

			# Labels
			desc_str = chr(ord('a') + m+2*fr)+') '+PLANNER_DOM[domain]+' '+titles[m]+' ('+PLANNER_DOM[planner]+', $f_{max} = %4.2f$)'%FRS[fr]
			xlabel = 'Processing Time (m)' if MINUTES and metric_x == 'Processing Time (s)' else metric_x
			ylabel = 'Processing Time (m)' if MINUTES and metric_y == 'Processing Time (s)' else metric_y
			plt.xlabel(xlabel+'\n'+desc_str,linespacing=2.0)
			plt.ylabel(ylabel)

			# Legend
			if m == 0 and fr == 0:
				legend = plt.legend(tnames, loc='lower center', ncol=10, scatterpoints=1, numpoints=1, fontsize=FONT_SIZE*0.75, bbox_to_anchor=(1.07,1.05))
				legend.get_frame().set_linewidth(LINE_WIDTH)

	plt.tight_layout()
	fig.subplots_adjust(top=0.85)
	for f in PLOT_FORMATS:
		plt.savefig(BOX_PLOT_NAME+domain+'_'+planner+'.'+f, bbox_inches='tight', pad_inches=PAD_INCHES)

def generate_single_box_plots(metrics):
	label_offset = BOX_LABEL_OFFSET
	for m,(title,metric_x,metric_y) in enumerate([('Quality','Makespan (s)', 'Number of Actions'),('Cost', 'Processing Time (s)', 'Memory Usage (GB)')]):

		fig = plt.figure(figsize=BOX_FIG_SIZE[domain][planner])
		set_fig_text_format()

		# Computing Pareto Domainance
		mean_dom = compute_pareto_domainance(metrics, TOOLS, metric_x, metric_y)

		# Setting up ordered plotting dataframe
		df = pd.DataFrame({
			'dom':		mean_dom,
			'tools':	TOOLS,
			'color':	[(0.000, 0.000, 0.000) for t in TOOLS],
			'rank':		[None for t in TOOLS],
		}).sort_values('dom',ascending=False)


		# Setting colors according to Pareto Domainance ranking
		unique = df['dom'].drop_duplicates().tolist()
		for k,v in COLOR_SCHEME.items():
			if k!=3 or sum([(domain==skip[0] and planner==skip[1] and m==skip[2]) for skip in FOURTH_BEST]):
				df.loc[df['dom']==unique[k],'color']	= pd.Series([v['color'] for x in df.index])
				df.loc[df['dom']==unique[k],'rank']		= pd.Series([v['rank'] for x in df.index])

		# Data
		mean_x	= [np.mean(metrics[metric_x]['sample']['Success (%)'][t]) for t in df['tools']]
		mean_y	= [np.mean(metrics[metric_y]['sample']['Success (%)'][t]) for t in df['tools']]

		# ax = plt.subplot2grid(subplot_layout, (0,0))

		# Mean Pareto Dominance
		for x, y, c, d in zip(mean_x, mean_y, df['color'], df['dom']):
			# plt.annotate(d, (x,y), xytext=label_offset, textcoords='offset points', fontsize=0.75*FONT_SIZE)
			plt.plot(x, y, ls='None', c=c, marker='o', ms=MARKER_SIZE)

		# # Plot limits
		# limits_x,limits_y = compute_box_limits(metrics, df['tools'], metric_x, metric_y)
		# ax.set_xlim(limits_x)
		# ax.set_ylim(limits_y)

		# Labels
		desc_str = chr(ord('a')+m)+') '+PLANNER_DOM[domain]+' '+title+' ('+PLANNER_DOM[planner]+')'+' Pareto Strength'
		xlabel = 'Processing Time (m)' if MINUTES and metric_x == 'Processing Time (s)' else metric_x
		ylabel = 'Processing Time (m)' if MINUTES and metric_y == 'Processing Time (s)' else metric_y
		plt.xlabel(xlabel,labelpad=1)
		plt.ylabel(ylabel,labelpad=1)

		# Table contents
		df = df.loc[df['rank'].notnull()]
		df['fmax'] = [format_tool_name('fusion-ratio',t) for t in df['tools']]
		df['tools'] = [format_tool_name('acro',t) for t in df['tools']]

		colLabels = ['Tool', '$f_{max}$', 'Pareto Strength']
		colLabels = ['Tool', '$f_{max}$', title+' Pareto Strength']
		# colLabels = ['Tool', '$f_{max}$', titles[m]]

		cell_text = df[['tools','fmax','dom']].values.tolist()

		num_rows = 1+len(cell_text)

		# Add a table at the bottom of the axes
		table = plt.table(
							cellText=cell_text,
							rowColours=df['color'].values,
							rowLabels=['\\textbf{%s}'%f for f in df['rank'].values],
							colLabels=['\\textbf{%s}'%f for f in colLabels],
							colWidths=[0.2,0.2,0.6],
							cellLoc='center',
							fontsize=24,
							bbox=[0.17, -num_rows*BOX_TABLE_ROW_SIZE-BOX_MARGIN, 0.83, num_rows*BOX_TABLE_ROW_SIZE],
						)
		for key,cell in table.get_celld().items():
			cell.set_linewidth(LINE_WIDTH)


		plt.tight_layout()
		for f in PLOT_FORMATS:
			plt.savefig(BOX_SINGLE_FIG_NAME+domain+'_'+planner+'_'+title.lower()+'.'+f, bbox_inches='tight', pad_inches=PAD_INCHES)

def get_stats(sample):
	if len(sample) < 2:
		return float('nan'), float('nan')
	mean = np.mean(sample)
	if SPREAD == 'STDEV':
		error = np.std(sample)
	if SPREAD == 'CI':
		error = 1.96*np.std(sample)/len(sample)**0.5
	return mean, error

# Gathering data
print 'Gathering data ...'
os.system(GATHER_DATA_SCRIPT)

# Filtering CSV file
print 'Filtering CSV file ...'
print RAW_STATS,FILTERED_STATS,file_header
StatsFilter.filter(RAW_STATS,FILTERED_STATS,file_header)

# Creating database
print 'Creating database ...'
df = pd.read_csv(FILTERED_STATS)

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
	for t in TOOLS:
		if metric == 'Planning Results (%)':
			status = df.loc[
							(df['Domain'] == domain) &
							(df['Planner'] == planner) &
							(df['Tool'] == t[0]) &
							(df['Fusion Ratio'] == t[1])
						]['Planning Results (%)'].values
			for f in STATUSES:
				if len(status):
					metrics[metric][f][t] = 100.0*len([k for k in status if k == STATUSES[f]['code']])/len(status)
				else:
					metrics[metric][f][t] = 0.0
		else:
			for f in STATUSES:
				sample = df.loc[
								(df['Domain'] == domain) &
								(df['Planner'] == planner) &
								(df['Tool'] == t[0]) &
								(df['Fusion Ratio'] == t[1]) &
								(df['Planning Results (%)'] == STATUSES[f]['code'])
							][metric].values
				sample = np.array([s/60.0 for s in sample]) if MINUTES and metric == 'Processing Time (s)' else sample
				mean, error = get_stats(sample)
				metrics[metric]['mean'][f][t]	= mean
				metrics[metric]['error'][f][t]	= error
				metrics[metric]['sample'][f][t]	= sample


# # Excel Fmax Table
# print 'Excel Box Spreadsheet ...'
# with open(FMAX_TABLE+domain+'_'+planner+'.tex', 'wb') as file:
# 	file.write(generate_fmax_table(metrics))


# # Excel Fmax Spreadsheet
# print 'Excel Fmax Spreadsheet ...'
# generate_excel_fmax('-'.join([EXCEL_FMAX,domain,planner])+'.xlsx',metrics)

# # Excel Spreadsheet
# print 'Excel Spreadsheet ...'
# generate_excel('-'.join([EXCEL_TABLE,domain,planner])+'.xlsx',metrics)

# # Stats Table
# print 'Stats Table ...'
# for metric in metrics:
# 	with open(STATS_TABLE+domain+'_'+planner+'_'+METRICS[metric]['flat']+'.tex', 'wb') as file:
# 		file.write(generate_stats_table(metrics,metric))

# # Stats Plots
# print 'Stats Plots ...'
# generate_stats_plots(metrics)

# # Fmax plots
# print 'Fmax plots ...'
# generate_fmax_plots(metrics)

# # Box Plots
# print 'Box Plots ...'
# generate_box_plots(metrics)

# Single Box Plots
print 'Single Box Plots ...'
generate_single_box_plots(metrics)
