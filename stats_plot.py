from CsvDatabase import *
import numpy as np
import matplotlib.pyplot as plt

def splot(q,xlabel,ylabel,title=''):
	labels = db.select(xlabel,q)
	aux = db.select(ylabel,q)
	values = []
	for e in aux:
		values.append(float(e))
	y_pos = np.arange(len(labels))
	plt.barh(y_pos, values, align='center', alpha=0.5)
	plt.yticks(y_pos, labels)
	plt.ylabel(xlabel)
	plt.xlabel(ylabel)
	plt.title(title) 
	plt.show()


def dplot(d,xlabel,ylabel,title=''):
	c = ['b','g','r','y','c','m']
	s = (2.0/3)
	w = s/len(d)
	for n,i in enumerate(d):
		labels = db.select(xlabel,d[i])
		y_pos = np.arange(len(labels))
		values = []
		for e in db.select(ylabel,d[i]):
			values.append(float(e))
		shift_pos = y_pos+w*n-(s/4)
		plt.barh(shift_pos, values, w, align='center', alpha=0.5, color=c[n], label=i)
	plt.ylabel(xlabel)
	plt.xlabel(ylabel)
	plt.yticks(y_pos, labels)
	plt.legend()	 
	plt.tight_layout()
	plt.title(title) 
	plt.show()

db = CsvDatabase('stats.csv')
print db.get_header()

xlabel = 'Tool'
ylabel = 'Makespan (s)'
for i in (range(0,3)):
	q = {}
	q['popf2'] = db.query([('Planner','popf2'),('Domain','push'),('Problem',str(i))])
	q['tfd'] = db.query([('Planner','tfd'),('Domain','push'),('Problem',str(i))])
	# q['colin'] = db.query([('Planner','colin'),('Domain','push'),('Problem',str(i))])
	# q['itsat'] = db.query([('Planner','itsat'),('Domain','push'),('Problem',str(i))])
	dplot(q,xlabel=xlabel,ylabel=ylabel,title=i)

# xlabel = 'Domain'
# ylabel = 'Makespan (s)'
# for i in ['popf2', 'tfd', 'itsat', 'colin']:
# 	q = {}
# 	q['0'] = db.query([('Planner',i),('Tool','CFP'),('Problem',str(0))])
# 	q['1'] = db.query([('Planner',i),('Tool','CFP'),('Problem',str(1))])
# 	q['2'] = db.query([('Planner',i),('Tool','CFP'),('Problem',str(2))])
# 	dplot(q,xlabel=xlabel,ylabel=ylabel,title=i)