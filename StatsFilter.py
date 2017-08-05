import re
import csv

FILTER_CHAR = '[/]'

class StatsFilter:

	# File input
	@staticmethod
	def __file_in(filename, delimiter=' ', quotechar='"'):
		with open(filename, 'rb') as f:
			ret_val = list(csv.reader(f, delimiter=delimiter, quotechar=quotechar))
		return ret_val

	# Filtering
	@staticmethod
	def __process(raw,header):
		ret_val = []
		ret_val.append(header)

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
			row_buffer.append(re.sub(FILTER_CHAR, '', row[5]))

			# Planner
			row_buffer.append(re.sub(FILTER_CHAR, '', row[9]))

			# Tool
			row_buffer.append(re.sub(FILTER_CHAR, '', row[11]))

			# Makespan
			row_buffer.append(re.sub(FILTER_CHAR, '', row[12]))

			# Actions
			row_buffer.append(re.sub(FILTER_CHAR, '', row[13]))

			# Proc. Time (s)
			row_buffer.append(re.sub(FILTER_CHAR, '', row[14]))

			# Memory (GB)
			mem = float(re.sub(FILTER_CHAR, '', row[15]))/1024
			row_buffer.append(str(mem))

			# Status
			row_buffer.append(re.sub(FILTER_CHAR, '', row[16]))

			ret_val.append(row_buffer)

		return ret_val

	# File output
	@staticmethod
	def __file_out(data, filename, delimiter=',', quotechar='"'):
		with open(filename, 'wb') as f:
			wr = csv.writer(f, delimiter=delimiter, quotechar=quotechar)
			for row in data:
				wr.writerow(row)

	# Wrapper function for the end user
	@staticmethod
	def filter(fname_in, fname_out, header, delimiter_in=' ', delimiter_out=',', quotechar='"'):
		raw = StatsFilter.__file_in(fname_in, delimiter=delimiter_in)
		filtered = StatsFilter.__process(raw,header)
		StatsFilter.__file_out(filtered,fname_out, delimiter=delimiter_out)
