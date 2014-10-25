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

docInfo = namedtuple('docInfo', ['doclen', 'max_tf'])

class Index():
    
    """
    attributes :

        Term_dict               : Dictionary with term as key and value as {df: int,docList:[]}

        Postings                : Dictionary with term as key and value as a dictionary which is 
                                  composed of docid as key and tf value.

        Doc_info                : Dictionary containg docid as key and namedtuple(doclen, max_tf)


    """

    __slots__ = ['Term_dict', 'Postings', 'Doc_info']

    def __init__(self):
        self.Term_dict = {}
        self.Postings = {}
        self.Doc_info = {}

    def size(self):
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
        docinfo = docInfo(doclen, max_tf)
        
        self.Doc_info[docid] = docinfo

        for term in self.Postings[docid]:
            self.Term_dict[term]['df'] += 1
            self.Term_dict[term]['docList'].append(docid)
