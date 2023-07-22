#
"""
Purpose of this code : convert assembly code to binary code
readable by a logisim rom
"""

import os
import argparse
from constants import *
from utils import *


def parse_line(line, num_line):

	binary_code = 0x0

	line = line.upper().replace('\n', '')
	#Line is :
	# - upper case
	# - without \n

	# LA RAM  A BESOIN D'UN CYCLE POUR SORTIR UNE DONNEE !
	# Donc pour faire A = SP ; *A = *A + 1 i faut faire :
	# A = SP
	# rien (par exemple un 2e A = SP)
	# *A = *A + 1


# Defines
	tokens = line.split(' ')
	tokens = [elt for elt in tokens if elt != ''] 
	if tokens[0] == 'DEFINE':
		if len(tokens) != 3:
			raise Exception(f"Error at instruction {num_line} : incorrect number of define parameters")
		try:
			int(tokens[2])
		except ValueError:
			raise Exception(f"Error at instruction {num_line} : define has to have an int value")
		try:
			int(token[1]) # if it is a number it is not a string and it's no good to have 2 defined as 3 !
			raise Exception(f"Error at instruction {num_line} : cannot define a number as something else !")
		except:
			DICT_DEFINES[tokens[1]] = int(tokens[2])
			return NOINSTR

	elif tokens[0] == 'LABEL':
		if len(tokens) != 2:
			raise Exception(f"Error at instruction {num_line} : incorrect number of label parameters. Expected 2 got {len(tokens)}")
		try:
			int(token[1]) # if it is a number it is not a string and it's no good to have 2 labeled as 3 !
			raise Exception(f"Error at instruction {num_line} : cannot define a number as something else !")
		except:
			DICT_DEFINES[tokens[1]] = num_line # the hex adress of the next instruction
			print(DICT_DEFINES['SP'])
			return NOINSTR



#jump (point virgule)
#TESTER
	if ';' in line:
		line, jump = line.split(';')
		print(line, jump)

		if line == jump == "": # NOP
			return NOP

		jump = jump.replace(' ', '')
		if jump.upper() not in JUMPS:
			raise Exception(f"Error at instruction {line} : {jump} is not a valid jump condition")

		binary_code |= JUMPS[jump] | I_ALU

		if(line == ""): # no computations to do, only jump
			return binary_code

# affectation (signe égal)
	if("=" in line):
		dest, source = line.replace("\n", "").split("=")


		# Extract destinations
		list_dest = dest.replace(" ", "").split(',') # get rid of spaces and commas
		for var in list_dest: 
			if not var in DESTINATIONS:
				raise Exception(f"Error instruction {line} : destination {var} is not valid")
			else:
				binary_code |= DESTINATIONS[var]



		# CHECK IF DATA INSTRUCTION

		# HARD NUMBER INITIALIZATION

		if source.replace(" ", "") in DICT_DEFINES:
			binary_code = op_initialization(DICT_DEFINES[source.replace(" ", "")], list_dest, num_line, binary_code)
			return binary_code
		try: 
			number = int(source.replace(" ", ""))
			binary_code = op_initialization(number, list_dest, num_line, binary_code)
			return binary_code

		except ValueError:
			word = source.replace(" ", "")
			if word in DICT_DEFINES:
				binary_code = op_initialization(DICT_DEFINES[word], list_dest, num_line, binary_code)
				return binary_code

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
	elif '^' in source:
		operation_type = XOR
	elif "~" in source:
		operation_type = NOT
	else: # operand affectation
		operation_type = OP_AFFECT


	""" DETERMINE DESTINATIONS AND DESTINATIONS"""

	# ADDITION
	if operation_type == ADD:
		gauche, droite = source.split("+")
		gauche, droite = gauche.replace(" ", ""), droite.replace(" ", "")
		if (gauche,droite) == ('A', '*A') or (gauche,droite) == ('*A', 'A'):
			raise Exception(f"Error at instruction {num_line} : can't operate on A and MEM at the same time")

		binary_code |= op_add(gauche, droite, num_line)

		return binary_code
		
	# - (including negations)
	#TESTER
	elif operation_type == SUB:
		gauche, droite = source.split("-")
		gauche, droite = gauche.replace(" ", ""), droite.replace(" ", "")
		if (gauche,droite) == ('A', '*A') or (gauche,droite) == ('*A', 'A'):
			raise Exception(f"Error at instruction {num_line} : can't operate on A and MEM at the same time")

		binary_code |= op_sub(gauche, droite, num_line)

		return binary_code

	# &
	# TESTER
	elif operation_type == AND:
		gauche, droite = source.split("&")
		gauche, droite = gauche.replace(" ", ""), droite.replace(" ", "")
		if (gauche,droite) == ('A', '*A') or (gauche,droite) == ('*A', 'A'):
			raise Exception(f"Error at instruction {num_line} : can't operate on A and MEM at the same time")

		binary_code |= op_and(gauche, droite, num_line)

		return binary_code

	# |
	# TESTER
	elif operation_type == OR:
		gauche, droite = source.split("|")
		gauche, droite = gauche.replace(" ", ""), droite.replace(" ", "")
		if (gauche,droite) == ('A', '*A') or (gauche,droite) == ('*A', 'A'):
			raise Exception(f"Error at instruction {num_line} : can't operate on A and MEM at the same time")

		binary_code |= op_or(gauche, droite, num_line)
 
		return binary_code


	elif operation_type == XOR:
		gauche, droite = source.split("^")
		gauche, droite = gauche.replace(" ", ""), droite.replace(" ", "")
		if (gauche,droite) == ('A', '*A') or (gauche,droite) == ('*A', 'A'):
			raise Exception(f"Error at instruction {num_line} : can't operate on A and MEM at the same time")

		binary_code |= op_xor(gauche, droite, num_line)
 
		return binary_code


	# ~
	#TESTER
	elif operation_type == NOT:
		gauche, droite = source.split('~')
		gauche, droite = gauche.replace(" ", ""), droite.replace(" ", "")
		if (gauche,droite) == ('A', '*A') or (gauche,droite) == ('*A', 'A'):
			raise Exception(f"Error at instruction {num_line} : can't operate on A and MEM at the same time")

		binary_code |= op_not(gauche, droite, num_line)

		return binary_code
			

	# affectation
	elif operation_type == OP_AFFECT:
		operand = source.replace(" ", "")
		binary_code |= op_affectation(operand, num_line)

	else:
		raise Exception(f"Error at instruction {line} : unrecognized operation")



	return binary_code


def write_binary(fichier, macros_path):
	code = "v3.0 hex words addressed\n"
	code += "0000:"

	intermediate = fichier.readlines()

	if(len(intermediate) > 2 ** 25):
		raise Exception("Error : program is too big (>2^25)")  # bon ça arrivera jamais

	# preprocess for macros and remove \n and comments
	lines = []
	for index, elt in enumerate(intermediate):
		path = macros_path + '/' + elt.replace(" ", "").replace("\n", "")
		if os.path.isfile(path):
			with open(path, 'r') as module:
				macro = module.readlines()
				for truc in macro:
					if truc != '\n' and not truc.startswith("//"):
						lines.append(truc)

		elif elt != '\n' and not elt.startswith("//"):
			lines.append(elt)


	num = 0
	for line in lines:
		instruction = format(parse_line(line, num), '04x') # the four last hex numbers 
		if instruction != format(NOINSTR, '04x'):
			code += " " + instruction
			num += 1

			if(num % 4 == 0): # 8 instructions per line, to keep it readable
				# would have liked to have 8 separated in 2 groups but then the file is interpreted wrong by logisim
				code += '\n'
				code += format(num, '04x') + ":" # get rid of '0x' at the beginning

	print(code)
	return code




if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("file", help="source code file to assemble")
	parser.add_argument("dest", nargs='?', default="", help="Destination file. If none will be the name of input file +/- extension")
	parser.add_argument("--macros", nargs='?', default=".")
	args = parser.parse_args()
	with open(args.file, 'r') as fichier:
		code = write_binary(fichier, args.macros)
		dest = args.dest if args.dest != "" else args.file.split(".")[0] + ".assembly"
		with open(dest, 'w') as f:
			f.write(code)
