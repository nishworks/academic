#!usr/bin/env python
#-*-coding:utf8-*-
"""
This is the main executable file for the project

"""

import os
import sys
import time
from query_parse import Query

if __name__ == '__main__':

    print "Welcome to document ranking system.\nPlease enter the query -"
    while(1):
        query = raw_input('>>')
        if query == 'exit':
            break
        q = Query(query)
        try:
            print q.ranked_w1[:10]
            print q.ranked_w2[:10]
        except Exception as e:
            print e
            print 'Query is not in acceptable format. Please try again.'