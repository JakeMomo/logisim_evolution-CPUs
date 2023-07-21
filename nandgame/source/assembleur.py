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

	line = line.upper()

#jump (point virgule)
#TESTER
	if ';' in line:
		line, jump = line.split(';')
		jump = jump.replace(' ', '').replace('\n', '')
		if jump.upper() not in JUMPS:
			raise Exception(f"Error at instruction {num_line+1} : {jump} is not a valid jump condition")
		binary_code |= JUMPS[jump]


# affectation (signe égal)
	if("=" in line):
		dest, source = line.replace("\n", "").split("=")


		# Extract destinations
		list_dest = dest.replace(" ", "").split(',') # get rid of spaces and commas
		for var in list_dest: 
			if not var.upper() in DESTINATIONS:
				raise Exception(f"Error instruction {num_line+1} : destination {var} is not valid")
			else:
				binary_code |= DESTINATIONS[var]



		# CHECK IF DATA INSTRUCTION

		# HARD NUMBER INITIALIZATION
		try: 
			number = int(source.replace(" ", ""))
			binary_code = op_initialization(number, list_dest, num_line, binary_code)

			return binary_code

		except ValueError:
			pass
	else:
		source = line.replace('\n', '')


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


	""" DETERMINE DESTINATIONS AND DESTINATIONS"""

	# ADDITION
	if operation_type == ADD:
		gauche, droite = source.split("+")
		gauche, droite = gauche.replace(" ", ""), droite.replace(" ", "")

		binary_code |= op_add(gauche, droite, num_line)

		return binary_code


		"""useless because addition, but may be useful for sub"""
		#if gauche.upper() != MAIN_ALU_REG: # we have to switch
		#	binary_code |= SW
		# for now there are only 2 registers so there is no ambiguity

		
	# - (including negations)
	#TESTER
	elif operation_type == SUB:
		gauche, droite = source.split("-")
		gauche, droite = gauche.replace(" ", ""), droite.replace(" ", "")

		binary_code |= op_sub(gauche, droite, num_line)

		return binary_code

	# &
	# TESTER
	elif operation_type == AND:
		gauche, droite = source.split("&")
		gauche, droite = gauche.replace(" ", ""), droite.replace(" ", "")

		binary_code |= op_and(gauche, droite, num_line)

		return binary_code

	# |
	# TESTER
	elif operation_type == OR:
		gauche, droite = source.split("|")
		gauche, droite = gauche.replace(" ", ""), droite.replace(" ", "")

		binary_code |= op_or(gauche, droite, num_line)

		return binary_code


	# ~
	#TESTER
	elif operation_type == NOT:
		gauche, droite = source.split('~')
		gauche, droite = gauche.replace(" ", ""), droite.replace(" ", "")

		binary_code |= op_not(gauche, droite, num_line)

		return binary_code
			

	# assignation
	elif operation_type == OP_AFFECT:
		operand = source.replace(" ", "")
		binary_code |= op_affectation(operand, num_line)

	else:
		raise Exception(f"Error at instruction {num_line+1} : unrecognized operation")



	return binary_code



def write_binary(fichier):
	code = "v3.0 hex words addressed\n"
	code += "0000:"

	lines = fichier.readlines()
	lines = [elt for elt in lines if elt != '\n' and not elt.startswith("//")]
	if(len(lines) > 2 ** 25):
		raise Exception("Error : program is too big (>2^25)")  # bon ça arrivera jamais

	num = 0
	for line in lines:
		code += " " + format(parse_line(line, num), '04x') # the four last hex numbers 
		num += 1

		if(num % 8 == 0): # 8 instructions per line
			code += '\n'
			code += format(num, '04x') + ":" # get rid of '0x' at the beginning


		elif(num % 4 == 0): # every 4 line a bonus space
			code += " "
		print(line)

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
