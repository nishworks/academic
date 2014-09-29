Readme.txt
==========

MACHINE 1000 - The microprocessor simulator !


Main Program :
	1. cpu.c

Compile Instructions:
	gcc cpu.c -o cpu

Execution:
	./cpu source_code_file

Sample source code files:

	1. add_3no.m1k - Users can enter three numbers to screen and get the sum.
	2. smiley.m1k - This file contains instruction set to print smiley.

	Note : These text files if open in windows, won't contain new line character.

Execution Details:
	This is the main program file. It can be compiled using a gcc compiler.
	On Unix/Linux -
	To compile write on a Unix/Linux bash : gcc cpu.c -o cpu1 
	This line will compile cpu to cpu1.
	
	To run the compiled file  :  ./cpu argument
	Argument = filename containing one instruction per line

	Argument is optional
	
	Case 1 -  Argument supplied
	========================
	This file takes argument as the path of the file including filename without parenthesis.
	For example :    ./cpu1 rest.txt   or   ./cpu  project/rest.txt  
	Where project is a directory containing file 'rest.txt'.
	
	When filename is incorrect ,program displays prompt to let user enter filename again.
	
	
	
	Case 2 - Argument not supplied or wrong argument value
	===============================================
	The program lets user enter filename even after running the program if user did not supply it in
	The arguments by giving a prompt.
	
	User can exit the program at the prompt by typing 'exit'
	

Instruction set

    1 = Load value           				Load the value into the AC         
    2 = Load address 						Load the value at the address into the AC
    3 = Store addr 							Store the value in the AC into the address
    4 = AddX 								Add the value in X to the AC
    5 = AddY								Add the value in Y to the AC
    6 = SubX								Subtract the value in X from the AC
    7 = SubY								Subtract the value in Y from the AC
    8 = Get port							If port=1, reads an int from the keyboard, stores it in the AC
    										If port=2, reads a char from the keyboard, stores it in the AC
    9 = Put port							If port=1, writes an int to the screen
											If port=2, writes a char to the screen				
   10 = CopyToX								Copy the value in the AC to X
   11 = CopyToY								Copy the value in the AC to Y
   12 = CopyFromX							Copy the value in X to the AC
   13 = CopyFromY							Copy the value in Y to the AC
   14 = Jump addr 							Jump to the address
   15 = JumpIfEqual addr 					Jump to the address only if the value in the AC is zero
   16 = JumpIfNotEqual addr 				Jump to the address only if the value in the AC is not zero
   17 = Call addr 							Push return address onto stack, jump to the address
   18 = Ret  								Pop return address from the stack, jump to the address
   19 = IncX  								Increment the value in X
   20 = DecX 								Decrement the value in X
   30 = End									End execution	