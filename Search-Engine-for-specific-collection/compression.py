#!usr/bin/env python
#-*-coding:utf8-*-
__doc__ = """

This module contain encoding methods which are the
basic methods in compression.

"""

from math import log,ceil
#from bitstring import BitArray
from bitarray import bitarray as BitArray
gf = 1.5
def gammaEncoding(number):
    return number
    if number == 1:
        return 0
    else:
        var = "{0:b}".format(number)
        offset =var[1:]
        length = len(offset)
        unary = ''
        for i in range(length):
            unary = unary.join(['1', ''])
        unary = unary.join(['', '0'])
 
        gammaCode = ''.join([str(unary), str(offset)])
        return gammaCode
 

def gamma(number):
 
    if number == 1:
        return 0
    else:
        var = "{0:b}".format(number)
        offset =var[1:]
        length = len(offset)
        unary = ''
        for i in range(length):
            unary = unary.join(['1', ''])
        unary = unary.join(['', '0'])
 
        gammaCode = ''.join([str(unary), str(offset)])
        return gammaCode

def deltaEncoding(number):
    return number
 
    if number == 1:
        return 0
    gap_bin = "{0:b}".format(number)
    length = len(gap_bin)
 
    led = gamma(length)
    gap_bin = gap_bin[1:]
 
    deltaCode = ''.join([str(led), str(gap_bin)])   
    return deltaCode
 
def bytes_needed(n):
    if n == 0:
        return 1
    return int(log(n,256)) + 1
 
def bytes(n):
    if n == 0:
        return 1
    return ceil(len(str(n))/8.0)

def round(num):
    return int(ceil(num*gf))