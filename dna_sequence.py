#!/usr/bin/env python3
# #############################################################################################################################################
# Introduction: 	This script will parse a file with nucleotide sequence data and print certain sequences.
#					Sequence is defined by a given start codon and a list of possible end codons.
#
# Usage: 			See help file for a list of usage examples:
# Syntax: 			py -3 dna_sequence.py --input "PIK3CA Nucleotide Sequence.txt" --debug
#
# Output:
# > py -3 dna_sequence.py --input "PIK3CA Nucleotide Sequence.txt" --debug
#   -I- Debug mode is on.
#   -I- Input file: PIK3CA Nucleotide Sequence.txt
#   -I- Output file: C:\Users\AllynH\Code\Git\dna_sequence\output[.txt|.csv]
#         -I- Found 632 codons
#         -I- Start codon: ATG Stop codons: ATT ATC ACT
# -I- Run time: 1.760136365890503 seconds
#
# # Version: 		V1.0
# Owner:			Allyn Hunt
#############################################################################################################################################
import sys, os, re, errno, gzip
import argparse, time
from datetime import datetime


#############################################################################################################################################
# Initialise global definitions:
#############################################################################################################################################
FILE_LIST = {
	"INPUT_FILE"		: "",
	"OUTPUT_FILE"		: "",
	"FIND_CODON"		: "",
	"CODON_SEQUENCE"	: ""
}
CWD = os.getcwd()

#############################################################################################################################################
# Initialise argparser:
#############################################################################################################################################
parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input",
					help="Input file.")

parser.add_argument("-o", "--output",
					help="Output file - will write as .txt and .csv (don't add a file extension).")

parser.add_argument("-f", "--find-codon",
					help="Find a value from a given codon.")

parser.add_argument("-si", "--sequence-index",
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
		FILE_LIST['OUTPUT_FILE'] = os.path.join(CWD, "output")

	if args.find_codon:
		FILE_LIST['FIND_CODON'] = int(args.find_codon)

	if args.sequence_index:
		FILE_LIST['CODON_SEQUENCE'] = int(args.sequence_index)

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

	codon_sequence = []

	for i, codon in enumerate(chunked_sequence):
		if codon == find_codon:
			codon_sequence.append((codon, i))

	print("\t-I- Found", len(codon_sequence), "codons")

	return True

#############################################################################################################################################

#############################################################################################################################################
# Parse DNA sequence into segments of 3 characters:
#############################################################################################################################################
def find_codon_with_index(chunked_sequence, find_codon, requested_sequence, codon_sequence):
	"""
	Take the chunked dna_sequence and find the start codon:
	"""

	# Sequence start + codon_index - 1, because we want the sequence start codon to be the first value:
	codon_index = (int(codon_sequence[requested_sequence]["START"]) + int(find_codon) -1)

	print("Here is the sequence:", codon_sequence[requested_sequence])
	print("Here is the start codon:", codon_sequence[requested_sequence]["START"])
	print("Here is the desired codons index:", codon_index)

	print("Here is the codon", find_codon, "places after sequence", requested_sequence)
	find_specific_codon(chunked_sequence, codon_index)

	new_sequence = []
	new_sequence = chunked_sequence[int(codon_sequence[requested_sequence]["START"]):int(codon_index) + 1:1]
	print("The new sequence is:", new_sequence)

	write_file("new_sequence", new_sequence)


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

	print("\t-I- Start codon:", start_codon, "Stop codons:", " ".join(stop_codon))

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
			# print("Sequence length is", len(current_sequence), "codons")
			# sequence_list.append(current_sequence)
			temp_dict['START']		= start_index
			temp_dict['STOP']		= i
			temp_dict['SEQUENCE']	= current_sequence
			sequence_list.append(temp_dict)
			current_sequence = []
			found_seq = False

	# print("Found", len(sequence_list), "matching sequences!")

	# print(sequence_list)

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

	return chunked_sequence

#############################################################################################################################################

#############################################################################################################################################
# Parse input file:
#############################################################################################################################################
def write_annotated_file(file_name, chunked_sequence, codon_sequence, file_type):
	"""
	Write the chunked codons into a file.
	If a sequence of codons is detected - it will print out the start codon index, stop codon index, the sequence length and the full sequence.
	"""

	if file_type == "txt":
		separator = " "
		file_name = FILE_LIST['OUTPUT_FILE'] + "_annotated" + ".txt"
	else:
		separator = ","
		file_name = FILE_LIST['OUTPUT_FILE'] + "_annotated" + ".csv"

	file_input = []

	for codon_chunk_index, codon_chunk in enumerate(chunked_sequence):
		for codon_index, codon in enumerate(codon_sequence):
			if codon_chunk_index == codon["START"]:
				seq_string = " ".join(codon['SEQUENCE'])
				message = "\nStart: {} Stop: {} Length: {} Sequence:{}{}\n".format(codon['START'], codon['STOP'], len(codon['SEQUENCE']), separator, seq_string)
				file_input.append(message)
		file_input.append(codon_chunk + separator)

	with open(file_name, 'wt') as output:
		for item in file_input:
			output.write(item)

	return True

#############################################################################################################################################

#############################################################################################################################################
# Parse input file:
#############################################################################################################################################
def write_file(file_name, chunked_sequence):
	"""
	Write the chunked codons into a .CSV file.
	If a sequence of codons is detected - it will print out the start codon index, stop codon index, the sequence length and the full sequence.
	"""

	separator = ","
	file_name = file_name + ".csv"

	print(len(chunked_sequence))
	# Add 1 because we are counting from 1, not 0:
	index = list(range(1, len(chunked_sequence) + 1))
	# print(index)

	print("\t-I- Writing file:", file_name)

	with open(file_name, 'wt') as output:
		for i in index:
			output.write(str(i) + separator)
		output.write("\n")
		for item in chunked_sequence:
			output.write(item + separator)

	return True

#############################################################################################################################################

#############################################################################################################################################
# Function for main program:
#############################################################################################################################################
def main_flow():
	if args.debug:
		start_time = time.time()

	parse_arguments()

	if args.debug is True:
		print("  -I- Input file:", FILE_LIST['INPUT_FILE'])
		print("  -I- Output file:", FILE_LIST['OUTPUT_FILE'] + "[.txt|.csv]")

	start_codon = "ATG"
	stop_codon = ["ATT", "ATC", "ACT"]

	dna_sequence		= parse_file(FILE_LIST['INPUT_FILE'])
	chunked_sequence	= parse_sequence(dna_sequence)
	find_codon_result	= find_codon(chunked_sequence, start_codon)
	codon_sequence 		= find_start_stop_codon(chunked_sequence, start_codon, stop_codon)

	# for i, c in enumerate(codon_sequence):
	# 	print("Sequence:", i, "contains:", len(c['SEQUENCE']), "codons.")
	# 	print("start:", c['START'], "Stop:", c['STOP'], "Sequence:", c['SEQUENCE'])

	write_file(FILE_LIST['OUTPUT_FILE'], chunked_sequence)
	write_annotated_file(FILE_LIST['OUTPUT_FILE'], chunked_sequence, codon_sequence, "txt")
	write_annotated_file(FILE_LIST['OUTPUT_FILE'], chunked_sequence, codon_sequence, "csv")

	if args.find_codon:
		# print("Finding:", args.find_codon)
		# find_specific_codon(chunked_sequence, FILE_LIST['FIND_CODON'])
		find_codon_with_index(chunked_sequence, FILE_LIST['FIND_CODON'], FILE_LIST['CODON_SEQUENCE'], codon_sequence)

	if args.debug:
		end_time = time.time() - start_time
		print("-I- Run time:", end_time, "seconds")

	return True
#############################################################################################################################################

#############################################################################################################################################
# Main program:
#############################################################################################################################################
if __name__ == "__main__":
	""" Run the main flow: """

	status = main_flow()
