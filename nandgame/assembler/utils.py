from constants import *



def op_add(gauche : str, droite : str, num_line: int) -> int:

	res = 0x0

	if gauche in OPERANDS and droite in OPERANDS:
		if gauche == '*A' or droite == '*A':
			res |= MEM_IN
		res |= ADD | I_ALU | OP_ARITHMETIC



	elif gauche in OPERANDS and not(droite in OPERANDS): # e.g A + 1
		try:
			number = int(droite)
			if number not in ADDABLE_NUMBERS:
				raise Exception(f"Error at instruction {num_line+1} : can't add value {droite} and register {gauche} directly")

			if gauche in MAIN_ALU_REG:
				res |= SW

			if gauche == '*A':
				res |= MEM_IN


			res |= ADDABLE_NUMBERS[number] | I_ALU | OP_ARITHMETIC

		except ValueError:
			raise Exception(f"Error instruction {num_line+1} : {droite} is not a number or valid regiter")


	elif not(gauche in OPERANDS) and droite in OPERANDS: # e.g 1 + A
		try:
			number = int(gauche)
			if number not in ADDABLE_NUMBERS:
				raise Exception(f"Error at instruction {num_line+1} : can't add value {gauche} and register {droite} directly")

			if gauche in MAIN_ALU_REG:
				res |= SW

			if droite == '*A':
				res |= MEM_IN

			res |= ADDABLE_NUMBERS[number] | I_ALU | OP_ARITHMETIC

		except ValueError:
			raise Exception(f"Error instruction {num_line+1} : {gauche} is not a number or valid regiter")


	elif not(gauche in OPERANDS) and not(droite in OPERANDS): # both DESTINATIONS are plain number, just add them
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
			raise Exception(f"Error at instruction {num_line+1} : {gauche} and {droite} are not valid destinations")

	return res


def op_sub(gauche: str, droite: str, num_line: int) -> int:
	res = 0x0

	if gauche in OPERANDS and droite in OPERANDS:
		res |= SUB | I_ALU | OP_ARITHMETIC
		if gauche in MAIN_ALU_REG:
			res |= SW
		return res 

	elif gauche in OPERANDS and not(droite in OPERANDS): # e.g A - 1
		try:
			number = - int(droite) # because we cropped '-' we have to add it manually
			if number not in ADDABLE_NUMBERS:
				raise Exception(f"Error at instruction {num_line+1} : can't sub value {droite} to register {gauche} directly")

			if gauche in MAIN_ALU_REG:
				res |= SW

			if gauche == '*A':
				res |= MEM_IN

			res |= ADDABLE_NUMBERS[number] | I_ALU | OP_ARITHMETIC

		except ValueError:
			raise Exception(f"Error instruction {num_line+1} : {droite} is not a number or valid regiter")

	# No 1 - A case, sorry losers

	elif not(gauche in OPERANDS) and droite in OPERANDS: # e.g -A (or 1 - A but it is not supported)
		# TODO replace by call to op_initialization

		if gauche != '' and gauche != '0':
			raise Exception(f"Error at instruction {num_line+1} : can't sub immediate value {gauche} to register {droite}")

		if droite not in OPERANDS:
			raise Exception(f"Error instruction {num_line+1} : {droite} is not a number or valid regiter")

		if droite not in MAIN_ALU_REG:
			res |= SW

		if droite == '*A':
			res |= MEM_IN

		res |= NOT | DESTINATIONS[droite] | OP_ARITHMETIC

	return res 



def op_and(gauche: str, droite: str, num_line: int) -> int:
	res = 0x0

	if not gauche in OPERANDS and droite in OPERANDS:
		raise Exception(f"Error at instruction {num_line+1} : both {gauche} and {droite} have to be valid operands in ({OPERANDS})")

	res |= AND | I_ALU | DESTINATIONS[droite] | OP_LOGIC
	return res


def op_or(gauche: str, droite: str, num_line: int) -> int:
	res = 0x0

	if not gauche in OPERANDS and droite in OPERANDS:
		raise Exception(f"Error at instruction {num_line+1} : both {gauche} and {droite} have to be valid operands in ({OPERANDS})")

	res |= OR | I_ALU | DESTINATIONS[droite] | OP_LOGIC
	return res



def op_not(gauche: str, droite: str, num_line: int) -> int:
	res = 0x0

	if gauche != "":
		raise Exception(f"Error at instruction {num_line+1} : negation takes one operand, not 2")

	res &= ~ZX_SW_FIELD # cancel potential switches and zeros
	if droite in MAIN_ALU_REG:
		#if operand=A, we have to switch to get A at the X port of logic unit
		res |= SW
	res |= NOT | I_ALU | OP_LOGIC

	return res



def op_affectation(operand: int, num_line: int) -> int:
	res = 0x0
	if operand in OPERANDS:
		res |= OPERANDS[operand] | I_ALU | OP_ARITHMETIC
		if operand not in MAIN_ALU_REG:
			res |= SW
	else:
		raise Exception(f"Error at instruction {num_line+1} : {operand} is not a valid operand")

	return res




def op_initialization(number : int, list_dest : list, num_line: int, binary_code: int) -> int:

	if number not in ADDABLE_NUMBERS:
		if not all(dest in SETABLE_REG for dest in list_dest): # you can't set all registers unfortunately
			raise Exception(f"Error instruction {num_line+1} : not all destinations {list_dest} are setable")

		if number > 2**(15) - 1: # can't load values greater than this in A
			raise Exception(f"Error instruction {num_line+1} : can't load value {res}, too big")

		binary_code &= I_DATA
		binary_code |= number
		binary_code |= I_DATA

	else:
		binary_code |= ADDABLE_NUMBERS[number] | ZERO | I_ALU

	return binary_code