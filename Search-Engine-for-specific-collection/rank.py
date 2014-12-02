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

def rank(query):

    q = Query(query)
    output = []
    try:
        output.append("Indexed form for query : %s" % q.indexedForm)
        output.append("As per W1 weight function :\n--------------------------")
        output.append("     Rank Doc ID   Score   Headline")
        i = 0
        for docid,score in  q.ranked_w1[:10]:
            i += 1
            output.append("     %-6i%-8i%-.5f  %-s" % (i, docid, score, headline(docid)))
        output.append("As per W2 weight function :\n--------------------------")
        output.append("     Rank Doc ID   Score   Headline")
        i = 0
        for docid,score in  q.ranked_w2[:10]:
            i += 1
            output.append("     %-6i%-8i%-.5f  %-s" % (i, docid, score, headline(docid)))
    except Exception as e:
        print e
        print 'Query is not in acceptable format. Please try again. %s ' % query
        sys.exit()

    return output



if __name__ == '__main__':


    if len(sys.argv) != 3:
        print "Please use this format. python rank.py pathToQueryFile pathToOutputFile"

    query_file = sys.argv[1]
    output_file = sys.argv[2]

    print "Welcome to document ranking system"
    print "Collection Size : %s\nAverage Doc length: %s \nPlease enter the query -" \
             % (str(get_collectionsize()), str(get_avgdoclen()))
    
    q = open(query_file,'r')
    f = open(output_file,'w')

    print "Reading Query file : %s" % query_file
    queries = [str(line.strip("\n").strip()) for line in q.readlines() if len(line) > 3]
    q.close()
    print "Total Queries %s" % len(queries)

    print "Starting processing queries..."
    i = 0
    for query in queries:
        i += 1
        print "Processing query %d  : %s" % (i,query)
        f.write("Query "+ str(i) +" : " + query + "\n")
        output = rank(query)
        for line in output:
            f.write(line+"\n")
        f.write("\n\n")
    f.close()

    # For command line Interface for query input. Set to false
    while(False):
        query = raw_input('>>')
        if query == 'exit':
            break
        rank(query)