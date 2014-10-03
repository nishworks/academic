#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# Author : Nishant Garg
# October 3, 2014

__doc__ = """
This module has only one method which takes two dictionaries and merge them into
a single dictionary.

Method Name : merge_two_dicts

Assumptions on input:
 * All keys are strings.
 * All values are integers.

Input can be from standard in, in which case we can user sys.stdin.readlines()
raw_input can also be used but it's deprecated and renamed in python3 to 'input'
Whereas sys.stdin.readlines is compatible in both the versions

For simplicity , currently this program takes predefined dictionaries as input.
dic_1 = {'d': 53, 're': 23, 'a': 44,}
dic_2 = {'b': 3, 'd' 32, 'were': 43,}

Ouput instructions:
 * output lines are sorted by key.
 * in event of a collision on keys between the two dictionaries, values
    as [value_from_first_dict, value_from_second_dict]

Output : 

Dict #1:        a -> 44
Dict #2:        b -> 3
Dict #1 & #2:   d -> [53, 32]
Dict #1:        re -> 23
Dict #2:        were: 43

"""

# Layman implementation for above problem
# Does not contain list or dictionary comprehensions
# Code readability
# Not so pythonic style

# This method takes O( len(dic1) + len(dic2) ) time to compute the merged dic as per
# the specifications in the problem statment
def mergeTwoDicts(dic1, dic2):

    # Marker to keep track which key is present in both dictionaries
    marker = {}
    merged_dic = {}
    for key in set(dic1.keys() + dic2.keys()):
        if dic1.has_key(key) & dic2.has_key(key):
            marker[key] = 3
        elif dic1.has_key(key):
            marker[key] = 1
        else:
            marker[key] = 2
    # Above code runs in O(m+n)
    # m = len(dic1), n = len(dic2)
    
    # Merging dictionaries
    for k,v in marker.iteritems():
        if v == 3:
            temp_list = list()
            temp_list.append(dic1[k])
            temp_list.append(dic2[k])
            merged_dic[k] = temp_list
        elif v == 1:
            merged_dic[k] = dic1[k]
        else:
            merged_dic[k] = dic2[k]
    # above operation takes O(m+n) time roughy, it actually takes O(len(marker)) time.

    return marker,merged_dic

# Dictionaries
dic_1 = {'d': 53, 're': 23, 'a': 44,}
dic_2 = {'b': 3, 'd' : 32, 'were': 43,}

# Method call
marker, merged = mergeTwoDicts( dic_1, dic_2)

# Printing part
for k,v in sorted(marker.iteritems()):
     if v != 3:
        print 'Dict #%d:        %s -> %d' % (v,k,merged[k])
     else:
        print 'Dict #1 & #2:   %s -> %s' % (k,str(merged[k]))