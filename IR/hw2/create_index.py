#!usr/bin/env python
#-*-coding:utf8-*-
"""


"""
import os
import sys

from filesystem import Directory, Doc
from nltk_wrapper import lemma_of, stem
from indexing import Index
import pickle

# Write serialize stuff here

if __name__ == '__main__':

    if not len(sys.argv) == 2:
        print 'Please enter the path to the directory and path to stop words file'
        sys.exit(0)

    dirPath = sys.argv[1]

    if not os.path.isdir(dirPath):
        print 'Not a valid directory path.Try Again'
        sys.exit(0)

    # Directory object
    directory = Directory(dirPath)

    print 'Processing documents in the {0} directory.'.format(dirPath)

    # Create Indexes
    index_1 = Index()
    index_2 = Index()

    for docPath in directory.docs_list:
        d = Doc(docPath)
        print 'Processing %s. Doclen: %d  ' % (d.docid,d.doclen)
        for token in d.tokens:
            lemmatized = lemma_of(token)
            stemmed = stem(token)
            index_1.update(lemmatized, d.docid)
            index_2.update(stemmed, d.docid)

        index_1.update_DocInfo(d.docid, d.doclen)

        #print 'Size of index1 after Doc%d : %d' %(d.docid, index_1.size())
        #print 'Size of index2 after Doc%d : %d' %(d.docid, index_2.size())
        index_2.update_DocInfo(d.docid, d.doclen)

    print 'end of program'

