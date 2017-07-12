import re
import csv

class StatsFilter:

	# File input
	@staticmethod
	def file_in(filename, delimiter=' ', quotechar='"'):
		with open(filename, 'rb') as f:
			ret_val = list(csv.reader(f, delimiter=delimiter, quotechar=quotechar))
		return ret_val

	# Filtering
	@staticmethod
	def process(raw):

		ret_val = []
		ret_val.append(['Domain','Problem','CFA','Planner','Tool','Makespan (s)','Actions','Proc. Time (s)','Memory (GB)','Status'])

		# File parsing
		for row in raw:

			row_buffer = []

			# Problem Name
			token = re.findall('(\w+)/problems/(P\d+C\d+)/', row[1])
			if len(token) > 0:
				token = token[0]
				row_buffer.append(token[0])
				row_buffer.append(token[1])

			# CFA
			row_buffer.append(row[5])

			# Planner
			row_buffer.append(row[9])

			# Tool
			row_buffer.append(row[11])

			# Makespan
			row_buffer.append(row[12])

			# Actions
			row_buffer.append(row[13])

			# Proc. Time (s)
			row_buffer.append(row[14])

			# Memory (GB)
			mem = float(row[15])/1024
			row_buffer.append(str(mem))

			# Status
			row_buffer.append(row[16])

			ret_val.append(row_buffer)

		return ret_val

	# File output
	@staticmethod
	def file_out(data, filename, delimiter=',', quotechar='"'):
		with open(filename, 'wb') as f:
			wr = csv.writer(f, delimiter=delimiter, quotechar=quotechar)
			for row in data:
				wr.writerow(row)

	# Wrapper function for the end user
	@staticmethod
	def filter(fname_in, fname_out, delimiter_in=' ', delimiter_out=',', quotechar='"'):
		raw = StatsFilter.file_in("stats.csv", delimiter=delimiter_in)
		filtered = StatsFilter.process(raw)
		StatsFilter.file_out(filtered, "stats_filtered.csv", delimiter=delimiter_out)
