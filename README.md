# nandgame_logisim

# Installation

## Install logisim-evolution
https://snapcraft.io/logisim-evolution-snapcraft

## download repo

# project organization
## source
Folder containing the logisim-evolution microprocessor

 ## assembler
 Folder containing the python assembler to convert assembly code to machine code

 # How to use
 To compile your source code (written following nandgame's assembly rules) type :
 python assembleur.py <source> <dest> 
 to upload the machine code to the rom, open the project in logisim and right-click on the rom part in the CPU file. Select "Edit content" and then "open" at the bottom. Select the machine code file you assembled and it's good.

 # Assembler instructions examples
 There are 2 registers A and D and one memory channel \*A. \*A is the memory value at RAM adress A. You can't use A and \*A together in any operation (multiplexer thing)

 ## arithmetic
 A = D + A
 A = \*A - D
 \*A = \*A - 1
 D = D + 1
 D = 0
 A = 1

 ## logic
 A = D & A
 A = \*A | D
 D = ~D

 ## jumps
 The program jumps at adresse A if the result of the previous operations validates the jump condition. E.g A = 0 ; JEQ jumps because the last op had an ALU resultequaling 0. You can right the jump in the same line as the computing or not.
 all possible jumps :
 - A = 0 ; JEQ
 - A = 3
   ; JGT
 - D = 1 ; JGE
 - D - D ; JLE // no need to actually store the result
 - D - 1 ; JLT
 - ; JEQ // unconditionnal jump

 Exception :
 A = 12 ; JMP // impoossible because all bits of the instruction are erased to store the immediate value, so no value assigning to A and jump in the same line

 # BEWARE
 The RAM needs 1 cycle to ouput data after the input adress changed ! E;G if you want to do :
 - A = SP
 - \*A = \*A + 1
 
 you have to skip a cycle in between (the way you want, this is an exemple) : 
 - A = SP
 // duplicate instruction
 - A = SP
 - *A = *A + 1