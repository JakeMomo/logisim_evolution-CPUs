import re
from constants import *

class CodeError(Exception):
	def __init__(self, num_line, message):
		self.message = f"Error at line {num_line} : " + message
		super().__init__(self.message)


def get_operand_int(operand: str, num_line: int, NO_SIZE_LIMIT=False):
	instruction = 0x0

	if operand in DICT_DEFINES:
		number = int(DICT_DEFINES[operand])

		if not(number >= 0 and number < 2**2):
			raise Exception(f"Error at line {num_line} : immediate operand has to be positive and less or equal to 3")

		instruction |= number

		return instruction, False

	else:
		try:
			number = int(operand)

			if not(number >= 0 and number < 2**2) and not(NO_SIZE_LIMIT):
				raise Exception(f"Error at line {num_line} : immediate operand has to be positive and less or equal to 3")

			instruction |= number

			return instruction, False

		except ValueError:
			raise Exception(f"Error at line {num_line} : immediate operand has to be an int (or you miswrote a register's name)")


def get_operand_mem(operand: str, num_line: int):
	instruction = 0x0

	pattern = re.compile(r"\[[A-Za-z]\]", re.IGNORECASE) # detect memory access, symbolized by [A]
	memory_used = bool(pattern.search(operand))

	reg = operand.replace("[", '').replace("]", '') # dégueu mais fonctionnel
	if reg not in REG: # remove bracket to check the register
		raise Exception(f"Error at line {num_line} : {operand} is not a valid operand (don't forget operand 1 has to be a reg)")

	instruction |= REG[reg]

	return instruction, memory_used