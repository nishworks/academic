#!usr/bin/env python
#-*-coding:utf8-*-
"""
This is the main executable file for the project

"""

import os
import sys
import time
from query_parse import Query
from index_load import get_collectionsize, get_avgdoclen, headline

if __name__ == '__main__':

    print "Welcome to document ranking system"
    print "Collection Size : %s\nAverage Doc length: %s \nPlease enter the query -" \
             % (str(get_collectionsize()), str(get_avgdoclen()))
    while(1):
        query = raw_input('>>')
        if query == 'exit':
            break
        q = Query(query)
        try:
            print "Indexed form for query : %s" % q.indexedForm
            print "As per W1 weight function :\n--------------------------"
            print "     Rank Doc ID   Score   Headline"
            i = 0
            for docid,score in  q.ranked_w1[:10]:
                i += 1
                print "     %-6i%-8i%-.5f  %-s" % (i, docid, score, headline(docid))
            print "As per W2 weight function :\n--------------------------"
            print "     Rank Doc ID   Score   Headline"
            i = 0
            for docid,score in  q.ranked_w2[:10]:
                i += 1
                print "     %-6i%-8i%-.5f  %-s" % (i, docid, score, headline(docid))
        except Exception as e:
            print e
            print 'Query is not in acceptable format. Please try again.'