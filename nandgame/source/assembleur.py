#
"""
Purpose of this code : convert assembly code to binary code
readable by a logisim rom
"""

import argparse
from constants import *
from utils import *


def parse_line(line, num_line):

	binary_code = 0x0

	split_line = line.split(" ")


#jump (point virgule)


# affectation (signe égal)
	if("=" in split_line):
		dest, source = line.replace("\n", "").split("=")


		# Extract destinations
		list_dest = dest.replace(" ", "").split(',') # get rid of spaces and commas
		for var in list_dest: 
			if not var.upper() in AFFECTABLE:
				raise Exception(f"Error instruction {num_line+1} : destination {var} is not valid")
			else:
				binary_code |= AFFECTABLE[var]



		# CHECK IF DATA INSTRUCTION

		# HARD NUMBER INITIALIZATION
		try: 
			number = int(source.replace(" ", ""))
			binary_code |= op_initialization(number, list_dest)

			return binary_code

		except ValueError:
			pass


# DETERMINE ALU OPERATION 
		operation_type = None
		if "+" in source:
			operation_type = ADD
		elif "-" in source:
			operation_type = SUB
		elif "&" in source:
			operation_type = AND
		elif "|" in source:
			operation_type = OR
		elif "~" in source:
			operation_type = NOT
		else: # operand affectation
			operation_type = OP_AFFECT


		""" DETERMINE AFFECTABLE AND DESTINATIONS"""

		# ADDITION
		if operation_type == ADD:
			gauche, droite = source.split("+")
			gauche, droite = gauche.replace(" ", ""), droite.replace(" ", "")

			binary_code |= op_add(gauche, droite)

			return binary_code


			"""useless because addition, but may be useful for sub"""
			#if gauche.upper() != MAIN_ALU_REG: # we have to switch
			#	binary_code |= SW
			# for now there are only 2 registers so there is no ambiguity

		
		# - (including negations)

		# constant 1 (and -1 ?)

		# &

		# |

		# ~

		# assignation
		elif operation_type == OP_AFFECT:
			operand = source.replace(" ", "")
			binary_code |= op_affectation(operand)

		else:
			raise Exception(f"Error at instruction {num_line+1} : unrecognized operation")


	return binary_code



def write_binary(fichier):
	code = "v3.0 hex words addressed\n"
	code += "0000:"

	lines = fichier.readlines()
	lines = [elt for elt in lines if elt != '\n']
	if(len(lines) > 2 ** 25):
		raise Exception("Error : program is too big (>2^25)")  # bon ça arrivera jamais

	num = 0
	print(lines)
	for line in lines:
		code += " " + format(parse_line(line, num), '04x') # the four last hex numbers 
		num += 1

		if(num % 8 == 0): # 8 instructions per line
			code += '\n'
			code += format(num, '04x') + ":" # get rid of '0x' at the beginning


		elif(num % 4 == 0): # every 4 line a bonus space
			code += " "

	print(code)
	return code




if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("file", help="source code file to assemble")
	parser.add_argument("dest", nargs='?', default="", help="Destination file. If none will be the name of input file +/- extension")
	args = parser.parse_args()
	with open(args.file) as fichier:
		code = write_binary(fichier)
		dest = args.dest if args.dest != "" else args.file.split(".")[0] + ".assembly"
		with open(dest, 'w') as f:
			f.write(code)
