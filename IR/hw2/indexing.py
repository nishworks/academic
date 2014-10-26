#!usr/bin/env python
#-*-coding:utf8-*-
__doc__ = """
This module creates the indexes for the documents.

    Some terms from information retrieval domain:
        df      : Document Frequency, Number of documents that the term occurs in
        tf      : Term Frequency, Number of times that the term occurs in each document
        docList : List of docs containing the Term
"""
from collections import namedtuple
from compression import *


class Index():
    
    """
    attributes :

        Term_dict               : Dictionary with term as key and value as {df: int,docList:[], total_freq int}

        Postings                : Dictionary with docid as key and value as a dictionary which is 
                                  composed of term as key and tf value.

        Doc_info                : Dictionary containg docid as key and dictionary {doclen, max_tf}


    """

    __slots__ = ['Term_dict', 'Postings', 'Doc_info', 'sizeinbytes']

    def __init__(self):
        self.Term_dict = {}
        self.Postings = {}
        self.Doc_info = {}
        self.sizeinbytes = 0


    def size(self):
        return len(self.Term_dict)

    def calcSize(self):

        for term in self.Term_dict:
            t = self.Term_dict[term]
            self.sizeinbytes += bytes_needed(t['df'])
            self.sizeinbytes += bytes_needed(t['total_freq'])
            for docid in t['docList']:
                self.sizeinbytes += bytes_needed(docid)

        for docid in self.Postings:
            doc = self.Postings[docid]
            self.sizeinbytes += bytes_needed(docid)
            for term in doc:
                self.sizeinbytes += bytes_needed(doc[term])

        for docid in self.Doc_info:
            doc = self.Doc_info[docid]
            self.sizeinbytes += bytes_needed(docid)
            self.sizeinbytes += bytes_needed(doc['doclen'])

    def calcInverted(self):
        return len(self.Term_dict)



    def update(self, term, docid):
        self.__update_Term_dict_with_total_Frequency(term)
        self.__update_Postings(term,docid)

    def __update_Term_dict_with_total_Frequency(self, term):

        if term not in self.Term_dict:
            self.Term_dict[term] = dict()
            self.Term_dict[term]['df'] = 0
            self.Term_dict[term]['docList'] = list()
            self.Term_dict[term]['total_freq'] = 0

        self.Term_dict[term]['total_freq'] += 1


    def __update_Postings(self, term, docid):
        if docid not in self.Postings:
            self.Postings[docid] = dict()

        if term not in self.Postings[docid]:
            self.Postings[docid][term] = 0
        
        self.Postings[docid][term] += 1



    def update_DocInfo(self, docid, doclen):
        """
        Run this method after all terms have been processing in the document,
        in the end.
        """

        max_tf = max(self.Postings[docid], key=self.Postings[docid].get)
        self.Doc_info[docid] = {'doclen':doclen, 'max_tf': max_tf}

        for term in self.Postings[docid]:
            self.Term_dict[term]['df'] += 1
            self.Term_dict[term]['docList'].append(docid)
            self.Term_dict[term]['docList'].sort()


    def getTerminfo(self, term):
        """
        df,tf,inverted list length in bytes

        """
        df = self.Term_dict[term]['df']
        tf_dict = {}
        for docid in self.Postings:
            tf = self.Postings[docid].get(term, 0)
            if tf != 0:
                tf_dict[docid] = tf
        doclist_len = len(self.Term_dict[term]['docList'])
        len_in_bytes = bytes_needed(doclist_len)

        return df,tf_dict,len_in_bytes


class IndexCompressed():
    """
    attributes :

        Term_dict               : Dictionary with term as key and value as {df: int,docList:[], total_freq}

        Postings                : Dictionary with docid as key and value as a dictionary which is 
                                  composed of term as key and tf value.

        Doc_info                : Dictionary containg docid as key and namedtuple(doclen, max_tf)


    """

    __slots__ = ['Term_dict', 'Postings', 'Doc_info', 'sizeinbytes']

    def __init__(self,index):
        self.Term_dict = {}
        self.Postings = {}
        self.Doc_info = {}
        self.sizeinbytes = 0

        self.compressTermDict(index)
        self.compressPostings(index)
        self.compressDocInfo(index)

    def calcSize(self):

        for term in self.Term_dict:
            t = self.Term_dict[term]
            self.sizeinbytes += bytes(t['df'])
            self.sizeinbytes += bytes(t['total_freq'])
            for docid in t['docList']:
                self.sizeinbytes += bytes(docid)

        for docid in self.Postings:
            doc = self.Postings[docid]
            self.sizeinbytes += bytes(docid)
            for term in doc:
                self.sizeinbytes += bytes(doc[term])

        for docid in self.Doc_info:
            doc = self.Doc_info[docid]
            #self.sizeinbytes += bytes(docid)
            self.sizeinbytes += bytes(doc['doclen'])

    def calulate_gapList(self,doclist):
        gaplist = []
        j = 0
        for docid in doclist:
            gap = docid - j
            j = docid
            gaplist.append(deltaEncoding(gap))
        return gaplist

    def compressTermDict(self,index):

        for term in index.Term_dict:
            self.Term_dict[term] = dict()
            self.Term_dict[term]['df'] = gammaEncoding(index.Term_dict[term]['df'])
            self.Term_dict[term]['total_freq'] = gammaEncoding(index.Term_dict[term]['total_freq'])
            
            doclist = index.Term_dict[term]['docList']
            self.Term_dict[term]['docList'] = self.calulate_gapList(doclist)

    def compressPostings(self,index):

        for docid in index.Postings:
            delta_docid = deltaEncoding(docid)
            self.Postings[delta_docid] = dict()

            for term in index.Postings[docid]:
                tf = gammaEncoding(index.Postings[docid][term])
                self.Postings[delta_docid][term] = tf

    def compressDocInfo(self,index):

        for docid in index.Doc_info:

            delta_docid = deltaEncoding(docid)
            doclen = gammaEncoding(index.Doc_info[docid]['doclen'])
            max_tf = index.Doc_info[docid]['max_tf']
            self.Doc_info[delta_docid] = {'doclen': doclen, 'max_tf': max_tf}



if __name__ == '__main__':

    print 'Please run create_index.py'