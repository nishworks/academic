#!usr/bin/env python
#-*-coding:utf8-*-
"""
This is the main executable file for the project

"""
import os
import sys
import time

from filesystem import Directory, Doc
from nltk_wrapper import lemma_of, stem
from indexing import Index, IndexCompressed
import pickle



if __name__ == '__main__':

    cmd = False
    file1 = 'Index_Version1'
    file2 = 'Index_Version1.compressed'
    file3 = 'Index_Version2'
    file4 = 'Index_Version2.compressed'
    outfile = 'output.txt'

    start_time = time.time()
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

    # Create Indexe objects version1 and version2
    index_1 = Index()
    index_2 = Index()

############## Index Generation ###############
    for docPath in directory.docs_list:
        d = Doc(docPath)
        print 'Processing %s. Doclen: %d  ' % (d.docid,d.doclen)
        for token in d.tokens:
            lemmatized = lemma_of(token)
            stemmed = stem(token)
            index_1.update(str(lemmatized), d.docid)
            index_2.update(str(stemmed), d.docid)

        index_1.update_DocInfo(d.docid, d.doclen)
        index_2.update_DocInfo(d.docid, d.doclen)
        #print '   Size of index1 after Doc%d : %d' %(d.docid, index_1.size())
        #print '   Size of index2 after Doc%d : %d' %(d.docid, index_2.size())

    print 'Preparing compressed indexes'

    index_1_compressed = IndexCompressed(index_1)
    index_2_compressed = IndexCompressed(index_2)

############## File Generation ###############
    print 'Generating files'
    f1 = open(file1, 'wb')
    f2 = open(file2, 'wb')
    f3 = open(file3, 'wb')
    f4 = open(file4, 'wb')

    pickle.dump(index_1,f1)
    f1.close()
    pickle.dump(index_1_compressed,f2)
    f2.close()
    pickle.dump(index_2,f3)
    f3.close()
    pickle.dump(index_2_compressed,f4)
    f4.close()


############# Size Calculation ################
    index_1.calcSize()
    index_1_compressed.calcSize()
    index_2.calcSize()
    index_2_compressed.calcSize()


############# Output #############


    output = open(outfile, 'w')
    s = []
    s.append("Size of index_1 uncompressed: %d" % index_1.sizeinbytes)
    s.append("Size of index_1_compressed : %d" % index_1_compressed.sizeinbytes)
    s.append("Size of index_2 uncompressed: %d" % index_2.sizeinbytes)
    s.append("Size of index_2_compressed : %d" % index_2_compressed.sizeinbytes)
    s.append("\n\n")
    s.append("Size of inverted list for Index version 1 : %d " % index_1.calcInverted() )
    s.append("Size of inverted list for Index version 2 : %d " % index_2.calcInverted()  )

    query_terms = ["Reynolds", "NASA", "Prandtl", "flow", "pressure", "boundary", "shock"]
    s.append("\n\n")

    for term in query_terms:
        term = str(stem(term.lower()))
        try:
            df, tf, len_in_bytes = index_2.getTerminfo(term)
            s.append('Getting value for %s' % stem(term))
            s.append('-----------------------------')
            s.append('     df                               : %d' % df)
            s.append('     Lenght of inverted list in bytes : %d' % len_in_bytes)
            s.append('     tf values for %s :' % stem(term))
            s.append('            Docid :  tf ')
            for docid in tf:
                s.append('                %s   :  %d ' % (docid, tf[docid]))
            s.append('\n')
        except:
            print 'Term does not exist in the documents, try another one.'

    s.append("--- %f seconds ---" % (time.time() - start_time) )

    for st in s:
        print st
        output.write(st)
        output.write('\n')
    output.close()

    x = ''
    while(cmd):
        x = raw_input('>>')
        
        if x == 'exit':
            break
        x = str(stem(x))
        try:
            df, tf, len_in_bytes = index_2.getTerminfo(x)
            print 'Getting values for %s' % (stem(x))
            print 'df : '
            print 'Lenght in bytes : %d' % len_in_bytes
        except:
            print 'Term does not exist in the documents, try another one.'
