#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# Author : Nishant Garg
# October 3, 2014

__doc__ = """

This module contains classes two perform string parsing.
The level of string parsing is just limited to counting the instances
of each string. The counts of each word also includes the count when a string
occurs in another string as a substring.

Input can be from standard in, in which case we can user sys.stdin.readlines()
raw_input can also be used but it's deprecated and renamed in python3 to 'input'
Whereas sys.stdin.readlines is compatible in both the versions

Also, input can be read from a file using open()

But for simplicity just using the test case from the problem statement

"""

inputStr = "this is a very very basic sentence and is only an abstract sample"

class StringParsingInit():

    """
        This class takes the input and develops the basic construct which
        can be used by different methods to apply operations.

        This class can contain input processing methods like
        STDIN , file read, support different delimiters, etc.

        Basic construct includes :
            List of words from the string (Includes Duplication)
            List of words from the string without duplication in a ascending order by length
            A dictionary initialized with 0 values for each word in set of words
    """

    def __init__(self, input_str):

        # Splitting words on space as delimiter
        self.wordSplits = input_str.split()        
        
        # Get the list of unique words in sorted order by length 
        self.setOfWords = set(self.wordSplits)
        self.setOfWords = sorted(self.setOfWords, key=len)

        # Initialize Dictionary to keep track of word counts
        self.wordCount = {k:0 for k in self.setOfWords}

        # This takes O(nlgn) time minimum and O(n**2) at max where n = number of unique words
        
class CountEachWordMethods(StringParsingInit):
    """
    This class contains the methods for counting each word in the input sequence, 
    which also takes into account if a word is present in another word as a subword.
    """

    def __init__(self, inputStr):
        StringParsingInit.__init__(self, inputStr)
        # Method Calls
        self.methodOne()
        print self.wordCount
    

    def methodOne(self):
        """
        This method takes O(number of words) + O(N**2) time == O(N**2) time

        """
        # Do the normal count, count occurance of each word
        for word in self.wordSplits:
            self.wordCount[word] += 1

        # Add to the each subword the count of each word it's present in
        # For example in out input string
        # count of is = 2, count of this = 1
        # so the updated count for 'is' = count of 'is' + count of 'this'
        for word in self.setOfWords:

            #if length of word is 1, there is no possible subword
            if len(word) == 1:
                continue
                
            # get the index of word in list
            idx = self.setOfWords.index(word)

            # Search for subwords that are present before that word in list
            # Also length of subword should less than word
            for sub_word in self.setOfWords[:idx]:
                if len(sub_word) < len(word) and sub_word in word:
                    self.wordCount[sub_word] += self.wordCount[word]

# Object creation
words = CountEachWordMethods(inputStr)