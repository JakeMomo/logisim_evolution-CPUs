#
"""
Purpose of this code : convert assembly code to binary code
readable by a logisim rom
"""

import argparse

#list of operands : registers in bank, memory, buffers...
OPERANDS = {'A':0x20 , 'D': 0x10 , '*A': 0x8}
AFFECTATIONS = {'A': 0x480, 'D': 0x4b0}
REG = set(['A', 'D'])

# if this register is not the first in an ALU operation, sw has to be activated
MAIN_ALU_REG = "D"
SETABLE_REG = {'A'}
ADDABLE_NUMBERS = {1:0x500, -1:0x700, 0:0x80} # the numbers that can be added directly to all registers

ADD = 0x400 
SUB = 0X600
AND = 0x0
OR = 0x100
NOT = 0x300 # add SW if reg is A
ZERO = 0x80
OP_AFFECT = 0x480

SW = 0x40
ZX = 0x80

I_DATA = 0x0 # useful...
I_ALU = 0x8000
REG_FIELD = 0x38



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
			if not var.upper() in OPERANDS:
				raise Exception(f"Error instruction {num_line+1} : destination {var} is not valid")
			else:
				binary_code |= OPERANDS[var]



		# CHECK IF DATA INSTRUCTION

		# HARD NUMBER INITIALIZATION
		try: 
			number = int(source.replace(" ", ""))
			if number not in ADDABLE_NUMBERS:
				if not all(dest in SETABLE_REG for dest in list_dest): # you can't set all registers unfortunately
					raise Exception(f"Error instruction {num_line+1} : not all destinations {list_dest} are setable")

				if number > 2**(15) - 1: # can't load values greater than this in A
							raise Exception(f"Error instruction {num_line+1} : can't load value {res}, too big")

				binary_code &= ~REG_FIELD # clean potential destinations that would false the value (just in case)
				binary_code |= number
				binary_code |= I_DATA

			else:
				binary_code |= ADDABLE_NUMBERS[number] | ZERO | I_ALU

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


		""" DETERMINE OPERANDS AND DESTINATIONS"""

		# ADDITION
		if operation_type == ADD:
			gauche, droite = source.split("+")
			gauche, droite = gauche.replace(" ", ""), droite.replace(" ", "")


			if gauche.upper() != MAIN_ALU_REG: # we have to switch
				binary_code |= SW
			# for now there are only 2 registers so there is no ambiguity


			if gauche in REG and droite in REG:
				binary_code |= ADD | I_ALU
				return binary_code


			elif gauche in REG and not(droite in REG): # e.g A + 1
				try:
					number = int(droite)
					if number not in ADDABLE_NUMBERS:
						raise Exception(f"Error at instruction {num_line+1} : can't add value {droite} and register {gauche} directly")

					binary_code |= ADDABLE_NUMBERS[number] | I_ALU

				except ValueError:
					raise Exception(f"Error instruction {num_line+1} : {droite} is not a number or valid regiter")


			elif not(gauche in REG) and droite in REG: # e.g 1 + A
				try:
					number = int(gauche)
					if number not in ADDABLE_NUMBERS:
						raise Exception(f"Error at instruction {num_line+1} : can't add value {gauche} and register {droite} directly")

					binary_code |= ADDABLE_NUMBERS[number] | I_ALU

				except ValueError:
					raise Exception(f"Error instruction {num_line+1} : {gauche} is not a number or valid regiter")


			elif not(gauche in REG) and not(droite in REG): # both operands are plain number, just add them
				try:
					un = int(gauche)
					deux = int(droite)
					res = un + deux

					if res > 2**(15) - 1: # can't load values greater than this in A
						raise Exception(f"Error at instruction {num_line+1} : can't load value {res}, too big")

					if not all(dest in SETABLE_REG for dest in list_dest): # you can't set all registers unfortunately
						raise Exception(f"Error at instruction {num_line+1} : not all destinations {list_dest} are setable")
					binary_code |= res
					binary_code |= I_DATA

				except ValueError:
					raise Exception(f"Error at instruction {num_line+1} : {gauche} and {droite} are not valid operands")

		
		# - (including negations)

		# constant 1 (and -1 ?)

		# &

		# |

		# ~

		# assignation
		elif operation_type == OP_AFFECT:
			operand = source.replace(" ", "")
			print(f"ligne {num_line} : ", operand)
			if operand in OPERANDS:
				binary_code |= OPERANDS[operand] | I_ALU
			else:
				raise Exception(f"Error at instruction {num_line+1} : {operand} is not a valid operand")

		else:
			raise Exception(f"Error at instruction {num_line+1} : unrecognized operation")


	return binary_code



def write_binary(fichier):
	code = "v3.0 hex words addressed\n"
	code += "0000:"

	lines = fichier.readlines()
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
