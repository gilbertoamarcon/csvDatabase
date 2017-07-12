from collections import namedtuple
import csv

class CsvDatabase:

	def __init__(self, filename, delimiter=',', quotechar='"'):

		# File reading
		with open(filename, 'rb') as csvfile:
			raw = list(csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar))

		# self.header parsing
		self.header = raw[0]
		for e in range(0,len(self.header)):
			self.header[e] = ''.join(c for c in self.header[e].split(" ") if c.isalnum())
		Entry = namedtuple("Entry", self.header)

		# Data parsing
		self.data = map(Entry._make, raw[1:])

	def query_r(self,key,value,data=None):
		if data is None:
			data = self.data
		return [entry for entry in data if entry._asdict()[key]==value]

	def query(self,select,data=None):
		q = self.query_r(select[0][0],select[0][1],data)
		if len(select) == 1:
			return q
		else:
			return self.query(select[1:],q)

	def select(self,key,data=None,as_integer=False,as_float=False):
		if data is None:
			data = self.data
		key = ''.join(c for c in key.split(" ") if c.isalnum())
		ret_val = []
		for d in data:
			e = d._asdict()[key]
			if as_integer:
				e = int(e)
			if as_float:
				e = float(e)
			ret_val.append(e)
		return ret_val

	def get_data(self):
		return self.data

	def get_header(self):
		return self.header