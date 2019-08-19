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


#############################################################################################################################################
# Initialise global definitions:
#############################################################################################################################################
FILE_LIST = {
	"INPUT_FILE"	: "",
	"OUTPUT_FILE"	: "",
	"FIND_CODON"	: ""
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

parser.add_argument("-f", "--find",
					help="Find a given codon.")

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

	if args.find:
		FILE_LIST['FIND_CODON'] = int(args.find)

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
	Remove all character returns and store as 1 lone string.
	Data is recieved like this and needs to be sanatised before continuing.
	"""

	open_function = gzip.open if file_name.endswith(".gz") else open
	with open_function(file_name,"rt", encoding='utf-8') as input_file:

		line = ""
		full_sequence = ""

		for line in input_file:
			if line.startswith(">"):
				continue
				# print(line)
				# line = re.sub("\>.*[0-9]", "", line)
				# print(line)
			line = re.sub("\n", "", line)

			# print(line)
			full_sequence = full_sequence + line


	return full_sequence

#############################################################################################################################################

#############################################################################################################################################
# Parse DNA sequence into segments of 3 characters:
#############################################################################################################################################
def find_codon(chunked_sequence, find_codon):
	"""
	Take the chunked dna_sequence and find the start codon:
	"""

	codon_list = []

	for i, codon in enumerate(chunked_sequence):
		if codon == find_codon:
			codon_list.append((codon, i))

	print("Found", len(codon_list), "codons")

	return True

#############################################################################################################################################

#############################################################################################################################################
# Parse DNA sequence into segments of 3 characters:
#############################################################################################################################################
def find_start_stop_codon(chunked_sequence, start_codon, stop_codon):
	"""
	Take the chunked dna_sequence and find the start codon:
	"""

	sequence_list = []
	current_sequence = []
	sequence_dict = {}
	start_index = 0

	found_seq = False

	print(start_codon, stop_codon)

	for i, codon in enumerate(chunked_sequence):
		# print(codon)
		if codon == start_codon:
			# print("Found start codon:", codon, "is item: ", i)
			found_seq = True
			start_index = i

		if found_seq:
			current_sequence.append(codon)

		if codon in stop_codon and found_seq:
			temp_dict = {}
			# print("Current codon:", codon, "stop_codons:", stop_codon)
			print("Sequence length is", len(current_sequence), "codons")
			# sequence_list.append(current_sequence)
			temp_dict['START']		= start_index
			temp_dict['STOP']		= i
			temp_dict['SEQUENCE']	= current_sequence
			sequence_list.append(temp_dict)
			current_sequence = []
			found_seq = False

	# print("Found", len(sequence_list), "matching sequences!")

	print(sequence_list)

	return sequence_list

#############################################################################################################################################

#############################################################################################################################################
# Parse DNA sequence into segments of 3 characters:
#############################################################################################################################################
def find_specific_codon(chunked_sequence, find_codon):
	"""
	Take the chunked dna_sequence and find the start codon:
	"""
	print("Finding codon:", chunked_sequence[int(find_codon)])


	return True

#############################################################################################################################################

#############################################################################################################################################
# Parse DNA sequence into segments of 3 characters:
#############################################################################################################################################
def parse_sequence(dna_sequence):
	"""
	Parse the DNA sequence into chunks of 3 characters.
	"""
	chunked_sequence = []
	chunk_size = 3


	chunked_sequence = [dna_sequence[i:i+chunk_size] for i in range(0, len(dna_sequence), chunk_size)]

	# print(chunked_sequence)

	print(len(chunked_sequence))

	return chunked_sequence

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

	start_codon = "ATG"
	stop_codon = ["ATT", "ATC", "ACT"]

	dna_sequence		= parse_file(FILE_LIST['INPUT_FILE'])
	chunked_sequence	= parse_sequence(dna_sequence)
	find_codon_result	= find_codon(chunked_sequence, start_codon)
	codon_list 			= find_start_stop_codon(chunked_sequence, start_codon, stop_codon)

	for i, c in enumerate(codon_list):
		print("Sequence:", i, "contains:", len(c['SEQUENCE']), "codons.")
		print("start:", c['START'], "Stop:", c['STOP'], "Sequence:", c['SEQUENCE'])

	if args.find:
		print("Finding:", args.find)
		find_specific_codon(chunked_sequence, FILE_LIST['FIND_CODON'])

	if args.debug:
		end_time = time.time() - start_time
		print("-I- Run time:", end_time, "seconds")

	return True

if __name__ == "__main__":
	""" Run the main flow: """

	status = main_flow()
