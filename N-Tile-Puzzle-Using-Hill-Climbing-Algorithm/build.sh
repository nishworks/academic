#!/bin/bash
# Compile Java Code. Main Class File - Hclimb.java

echo "Testing Hill Climb Program"
javac Hclimb.java


#Run Java Code
# java ClassName Arguments

java Hclimb 1,2,3,7,8,5,0,6,4				# To print values to STD Output
java Hclimb 1,2,3,8,6,4,0,7,5 > output.txt  # To direct ouput to file
