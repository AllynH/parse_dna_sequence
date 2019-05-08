#!/usr/bin/env python3
# #############################################################################################################################################
# Introduction: 	This script will parse a file and do some stuff.
#
# Usage: 			See help file for a list of usage examples:
# Syntax: 			python script_example.py --input input.txt
#
# Output:
#
# > script_example.py -i README.md --debug
#	-I- Debug mode is on.
# 		-I- Input file: README.md
#		-I- Output file: /path/to/dir/output.txt
# HELLO: this is a test
#
# # Version: 		V1.0
# Owner:		Allyn Hunt
#############################################################################################################################################
import sys, os, re, errno, gzip
import argparse, time
from datetime import datetime
from run_subprocess_functions import *


#############################################################################################################################################
# Initialise global definitions:
#############################################################################################################################################
FILE_LIST = {
	"INPUT_FILE"	: "",
	"OUTPUT_FILE"	: ""
}
CWD = os.getcwd()

#############################################################################################################################################
# Initialise argparser:
#############################################################################################################################################
parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input",
					help="Input file.")

parser.add_argument("-o", "--output",
					help="Output file.")

parser.add_argument("-d", "--debug", action="store_true", default=False,
					help="Prints debug information.")

args = parser.parse_args()
#############################################################################################################################################

#############################################################################################################################################
# Set user defined input options:
#############################################################################################################################################
def parse_arguments():
	""" Parse arguments and select default arguments """

	# Input file:
	if args.input:
		FILE_LIST['INPUT_FILE'] = args.input

	# Output tuple list:
	if args.output:
		FILE_LIST['OUTPUT_FILE'] = args.output
	else:
		FILE_LIST['OUTPUT_FILE'] = os.path.join(CWD, "output.txt")

	# Print debug information:
	if args.debug is True:
		print("  -I- Debug mode is on.")

	return True
#############################################################################################################################################

#############################################################################################################################################
# Parse input file:
#############################################################################################################################################
def parse_file(file_name):
	"""
	Parse an input file.
	Write all fail information to unique files, with a meaningful name based on pattern information.
	"""

	open_function = gzip.open if file_name.endswith(".gz") else open
	with open_function(file_name,"rt", encoding='utf-8') as input_file:

		for line in input_file:
			if line.startswith("hello:"):
				line = re.sub("hello", "HELLO", line)
				print(line)

	return True

#############################################################################################################################################

#############################################################################################################################################
# Set user defined input options:
#############################################################################################################################################
def main_flow():
	if args.debug:
		start_time = time.time()

	parse_arguments()

	if args.debug is True:
		print("  -I- Input file:", FILE_LIST['INPUT_FILE'])
		print("  -I- Output file:", FILE_LIST['OUTPUT_FILE'])

	parse_file(FILE_LIST['INPUT_FILE'])

	if args.debug:
		end_time = time.time() - start_time
		print("-I- Run time:", end_time, "seconds")

	return True

if __name__ == "__main__":
	""" Run the main flow: """

	status = main_flow()
	