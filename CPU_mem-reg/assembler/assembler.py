

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

	index = line.index(' ') # the first space separates instruction from operands
	instr = line[:index].replace(' ', '')



# Defines
	if instr == 'DEFINE':
		operands = line[index+1:].split(' ')
		if len(operands) != 2:
			raise Exception(f"Error at instruction {num_line} : incorrect number of define parameters")
		try:
			int(operands[1])
		except ValueError:
			raise Exception(f"Error at instruction {num_line} : define has to have an int value")
		try:
			int(operands[0]) # if it is a number it is not a string and it's no good to have 2 defined as 3 !
			raise Exception(f"Error at instruction {num_line} : cannot define a number as something else !")
		except:
			DICT_DEFINES[operands[0]] = int(operands[1])
			return NOINSTR

	elif instr == 'LABEL':
		if len(operands) != 1:
			raise Exception(f"Error at instruction {num_line} : incorrect number of label parameters. Expected 1 got {len(tokens)}")
		try:
			int(operands[0]) # if it is a number it is not a string and it's no good to have 2 labeled as 3 !
			raise Exception(f"Error at instruction {num_line} : cannot define a number as something else !")
		except:
			DICT_DEFINES[operands[0]] = num_line # the hex adress of the next instruction
			print(DICT_DEFINES['SP'])
			return NOINSTR




	if not instr in INSTRUCTIONS:
		raise CodeError(num_line, f"instruction {instr} is not supported")


	operands = line[index:].replace(' ', '').split(',')

	binary_code |= INSTRUCTIONS[instr]

	if instr == 'SET':
		if(len(operands) != 2):
			raise CodeError(num_line, f"SET needs 2 operands")
		if not operands[0] in REG:
			raise CodeError(num_line, f"{operands[0]} is not a valid destination for SET instruction")

		num, mem_used = get_operand_int(operands[1], num_line, NO_SIZE_LIMIT = True)

		if mem_used:
			raise CodeError(num_line, "cannot use SET with a non int value")

		binary_code |= num

	elif instr == 'JMP':

		if len(operands) == 1: # unconditional jump
			dest, mem_used_src = get_operand_mem(operands[0], num_line)
			print(dest)
			binary_code |= dest << POS_SRC2
			if mem_used_src:
				binary_code |= R_MEM

		else:
			if len(operands) != 2:
				raise CodeError(num_line, f"conditional jump accepts 2 operands")

			dest, mem_used_src = get_operand_mem(operands[0], num_line)
			binary_code |= dest << POS_SRC2
			if mem_used_src:
				binary_code |= R_MEM

			try:
				nb = int(operands[1])
				if(nb < 0 or nb > 7):
					raise CodeError(num_line, f"jump condition must be between 1 and 7 included")
				binary_code |= nb

			except ValueError:
				raise CodeError(num_line, f"Jump operand has to be an int between 1 and 7 included")


	elif instr == "CMP":
		if len(operands) != 2:
			raise CodeError(num_line, f"cmp instruction takes 2 operands")

		# get src1, int or reg
		try:
			src1, mem_used_src1 = get_operand_int(operands[0], num_line)
			binary_code |= I_1

		except:
			src1, mem_used_src1 = get_operand_mem(operands[0], num_line)


		# get src2, int or register
		try:
			src2, mem_used_src2 = get_operand_int(operands[1], num_line)
			binary_code |= I_2

		except:
			src2, mem_used_src2 = get_operand_mem(operands[1], num_line)

		if (mem_used_src1 + mem_used_src2 >= 2):
			raise Exception(f"Error at line {num_line} : cannot have more than one memory operand per instruction")

		binary_code |= src1 << POS_SRC1 | src2 << POS_SRC2

		if mem_used_src2 or mem_used_src1:
			binary_code |= R_MEM



	elif instr in BINARY_INSTR:
		if len(operands) != 3: # 1 dest and 2 src
			raise Exception(f"Error at line {num_line} : instruction {instr} expects 3 operands but got {len(operands)} : {operands}")

		# get dest
		dest, mem_used_dest = get_operand_mem(operands[0], num_line)

		# get src1, int or reg
		try:
			src1, mem_used_src1 = get_operand_int(operands[1], num_line)
			binary_code |= I_1

		except:
			src1, mem_used_src1 = get_operand_mem(operands[1], num_line)


		# get src2, int or register
		try:
			src2, mem_used_src2 = get_operand_int(operands[2], num_line)
			binary_code |= I_2

		except:
			src2, mem_used_src2 = get_operand_mem(operands[2], num_line)

		if (mem_used_dest + mem_used_src1 + mem_used_src2 == 2):
			if not(mem_used_dest) or (dest != src1 and mem_used_src1) or (dest != src2 and mem_used_src2): #cannot have 2 mem operands, only 1 operand and 1 dest that are the same
				raise Exception(f"Error at line {num_line} : cannot have two different memory operands in an instruction")
			
		elif (mem_used_dest + mem_used_src1 + mem_used_src2 > 2):
			raise Exception(f"Error at line {num_line} : cannot have two different memory operands in an instruction")


		binary_code |= dest << POS_DEST | src1 << POS_SRC1 | src2 << POS_SRC2

		if mem_used_dest:
			binary_code |= W_MEM

		if mem_used_src1:
			binary_code |= R_MEM | MEM_OPERAND_1
		elif mem_used_src2:
			binary_code |= R_MEM | MEM_OPERAND_2



	elif instr in UNARY_INSTR:
		if len(operands) != 2:
			raise CodeError(num_line, f"instruction {instr} expects 2 operand but got {len(operands)} : {operands}")

		# get dest
		dest, mem_used_dest = get_operand_mem(operands[0], num_line)

		# get src1, int or reg
		try:
			src1, mem_used_src1 = get_operand_int(operands[1], num_line)
			binary_code |= I_1

		except:
			src1, mem_used_src1 = get_operand_mem(operands[1], num_line)


		if (mem_used_dest + mem_used_src1 == 2):
			if not(mem_used_dest) or (dest != src1 and mem_used_src1) or (dest != src2 and mem_used_src2): #cannot have 2 mem operands, only 1 operand and 1 dest that are the same
				raise Exception(f"Error at line {num_line} : cannot have two different memory operands in an instruction")

		binary_code |= dest << POS_DEST | src1 << POS_SRC1

		if mem_used_dest:
			binary_code |= W_MEM
		if mem_used_src1:
			binary_code |= R_MEM




	return binary_code


def write_binary(fichier, macros_path):
	code = "v3.0 hex words addressed\n"
	code += "0000:"

	intermediate = fichier.readlines()

	lines = []
	for index, elt in enumerate(intermediate):
		path = macros_path + '/' + elt.replace(" ", "").replace("\n", "")
		if os.path.isfile(path):
			with open(path, 'r') as module:
				macro = module.readlines()
				for truc in macro:
					if truc != '\n' and not truc.startswith("//"):
						lines.append(truc)

		elif elt != '\n' and not elt.startswith("//"): # macro
			lines.append(elt)

	num = 0
	for line in lines:
		instruction = format(parse_line(line, num), '04x') # the four last hex numbers 
		if instruction != format(NOINSTR, '04x'):
			code += " " + instruction
			num += 1

			if(num % 4 == 0): # 4 instructions per line, to keep it readable
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
