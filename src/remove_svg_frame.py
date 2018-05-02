#!/usr/bin/python
import re
import argparse

# Main
def main():

	# Parsing user input
	parser = argparse.ArgumentParser()
	parser.add_argument(
			'-i','--input',
			nargs='?',
			required=True,
			help='Input file name.',
		)
	parser.add_argument(
			'-o','--output',
			nargs='?',
			required=True,
			help='Output file name.',
		)
	args = parser.parse_args()

	# Reading file
	with open(args.input,'rb') as f:
		data = f.read()

	# Filtering
	data = re.sub('\s*<g\s+id\s*=\s*"(id\d+:)*patch_1"\s*>(:?(?!</g>)[\S\s])+</g>', '', data)

	# Storing results
	with open(args.output,'wb') as f:
		f.write(data)



if __name__ == "__main__":
	main()

