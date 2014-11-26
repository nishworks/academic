#!usr/bin/env python
#-*-coding:utf8-*-

import pickle

_f1 = open('Index_Version1', 'r')
_f2 = open('Index_Version2', 'r')
_f3 = open('headlines', 'r')

_index_version1 = pickle.load(_f1)
_index_version2 = pickle.load(_f2)
_headlines = pickle.load(_f3)

_f1.close()
_f2.close()
_f3.close()

_index = _index_version2

_collectionSize = len(_index.Doc_info)
_avgDocLen = 0

for docid,dic in _index.Doc_info.items():
    _avgDocLen += dic['doclen']

_avgDocLen /= _collectionSize


#Helper methods for index information
def get_docList(token):
    try:
        return _index.Term_dict[token]['docList']
    except:
        return []

def get_df(token):
    try:
        return float(_index.Term_dict[token]['df'])
    except:
        return 0

def get_tf(token,doc):
    try:
        return float(_index.Postings[doc][token])
    except:
        return 0

def get_doclen(doc):
    return float(_index.Doc_info[doc]['doclen'])

def get_maxtf(doc):
    maxtf = _index.Doc_info[doc]['max_tf']
    return get_tf(maxtf, doc)

def get_collectionsize():
    return float(_collectionSize)

def get_avgdoclen():
    return float(_avgDocLen)

def headline(doc):
    return _headlines[doc].strip("<TITLE>").strip().strip("\n").strip(".")[:50]





