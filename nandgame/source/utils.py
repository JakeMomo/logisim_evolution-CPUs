from constants import *



def op_add(gauche : str, droite : str) -> int:

	res = 0x0

	if gauche in REG and droite in REG:
				res |= ADD | I_ALU


	elif gauche in REG and not(droite in REG): # e.g A + 1
		try:
			number = int(droite)
			if number not in ADDABLE_NUMBERS:
				raise Exception(f"Error at instruction {num_line+1} : can't add value {droite} and register {gauche} directly")

			res |= ADDABLE_NUMBERS[number] | I_ALU

		except ValueError:
			raise Exception(f"Error instruction {num_line+1} : {droite} is not a number or valid regiter")


	elif not(gauche in REG) and droite in REG: # e.g 1 + A
		try:
			number = int(gauche)
			if number not in ADDABLE_NUMBERS:
				raise Exception(f"Error at instruction {num_line+1} : can't add value {gauche} and register {droite} directly")

			res |= ADDABLE_NUMBERS[number] | I_ALU

		except ValueError:
			raise Exception(f"Error instruction {num_line+1} : {gauche} is not a number or valid regiter")


	elif not(gauche in REG) and not(droite in REG): # both AFFECTABLE are plain number, just add them
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
			raise Exception(f"Error at instruction {num_line+1} : {gauche} and {droite} are not valid AFFECTABLE")

	return res



def op_affectation(operand: int) -> int:

	res = 0x0

	if operand in OPERANDS:
		res |= OPERANDS[operand] | I_ALU
		if operand != MAIN_ALU_REG:
			res |= SW
	else:
		raise Exception(f"Error at instruction {num_line+1} : {operand} is not a valid operand")

	return res




def op_initialization(number : int, list_dest : list) -> int:

	res = 0x0

	if number not in ADDABLE_NUMBERS:
		if not all(dest in SETABLE_REG for dest in list_dest): # you can't set all registers unfortunately
			raise Exception(f"Error instruction {num_line+1} : not all destinations {list_dest} are setable")

		if number > 2**(15) - 1: # can't load values greater than this in A
			raise Exception(f"Error instruction {num_line+1} : can't load value {res}, too big")

		res &= ~REG_FIELD # clean potential destinations that would false the value (just in case)
		res |= number
		res |= I_DATA

	else:
		res |= ADDABLE_NUMBERS[number] | ZERO | I_ALU

	return res