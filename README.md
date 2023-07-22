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