
#list of affectables (left of '='') : registers in bank, memory, buffers...
AFFECTABLE = {'A':0x20 , 'D': 0x10 , '*A': 0x8}
#list of operands (right of '=')
OPERANDS = {'A': 0x480, 'D': 0x4b0, '*A': 0x94}
REG = set(['A', 'D'])

# if this register is not the first in an ALU operation, sw has to be activated
MAIN_ALU_REG = "A"
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