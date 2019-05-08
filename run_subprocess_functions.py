# #############################################################################################################################################
# Introduction: 	This file contains generic functiuons to run SubProcess commands
#
# Usage: 		from run_subprocess_functions import *
# Syntax: 		output = run_subprocess_command(command)
# 
# Output:		N/A
# Version: 		V1.0
# Owner:		Allyn Hunt
#############################################################################################################################################

import sys, re
import subprocess
from subprocess import PIPE

def run_subprocess_command(command_string, debug_flag):
	""" Runs a subprocess command. """
	try:
		output = subprocess.check_output(command_string.split()).decode('utf-8')
	except subprocess.CalledProcessError as output:
		print("-E- subprocess.CalledProcessError")
		print(output)
	return output
