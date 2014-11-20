N-Tile Puzzle solving using Hill Climing algorithm

Example: http://www.tilepuzzles.com/default.asp?p=12

In this problem, an N-tile puzzle is given. Let's take a 8-Tile puzzle:

	Puzzle 		       Goal
	5 | 2 | 3	    1 | 2 | 3 
	---------           ---------
	8 | 6 | 0     =>    8 | 0 | 4
	---------           ---------
	4 | 7 | 1           7 | 6 | 5

While reaching goal program prints all the states, sample output is in output.txt
The program solves the 8-Tiles puzzle using hill-climbing search algorithm.

The implementation of the algorithm is in file Hclimb.java
Class Hclimb parses the input in its main function. 
Class State represents tile positions on each step.
Class Snode is data Wrapper which consists of State, Depth, cost(manhattan Distance) and parent node.

The code has plenty of comments for techincal details.

The program was tested using Java 7.

The build script can be run as follows. 

----------------------
bash ./build.sh
----------------------
