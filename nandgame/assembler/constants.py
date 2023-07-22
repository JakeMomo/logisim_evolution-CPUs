
#list of affectables (left of '='') : registers in bank, memory, buffers...
DESTINATIONS = {'A':0x20 , 'D': 0x10 , '*A': 0x8}

#list of operands (right of '=')
OPERANDS = {'A': 0x80, 'D': 0xc0, '*A': 0x1080}

REG = set(['A', 'D'])

#list of available jump conditions
JUMPS = {"JMP":0x7, "JGE":0x3, "JLE":0x6, "JGT":0x1, "JEQ":0x2, "JLT":0x4}

# if these register is not the first in an ALU operation, sw has to be activated
MAIN_ALU_REG = {'A', '*A'}
SETABLE_REG = {'A'}
ADDABLE_NUMBERS = {1:0x500, -1:0x700, 0:0x80} # the numbers that can be added directly to all registers

ADD = 0x400 
SUB = 0X600
NEG = 0x680
AND = 0x0
OR = 0x100
XOR = 0x200
NOT = 0x300 # add SW if reg is A
ZERO = 0x80
OP_AFFECT = 0x480
NOP = 0x8000
NOINSTR = 0xFFFF

MEM_IN = 0x1000
SW = 0x40
ZX = 0x80
ZX_SW_FIELD = SW | ZX

I_DATA = 0x0 # useful...
OP_LOGIC = 0x000
OP_ARITHMETIC = 0x400 # useful...
I_ALU = 0x8000
REG_FIELD = 0x38

DICT_DEFINES = {}
