#!usr/bin/env python
#-*-coding:utf8-*-

__doc__ = """
This module has the classes which provide the helper
methods to parse a query and return the stem-set.
    stop_words              : List of stop words going to be used in program
"""
import os
import sys
import re
from nltk_wrapper import stem
from index_load import *
import math
import operator

stop_words = []
#Calulate stop words
with open('stopwords', 'r') as file:
    for line in file:
        stop_words.append(line[:-1].strip())

stop_words = set(stop_words)

def log(num):
    return math.log(num, 2)


class Query():

    def __init__(self, query):
        #query  = query.replace('-', ' ')
        self.tokens = self.parse(query)
        self.indexedForm = ' '.join(self.tokens)
        self.docs = self.get_docs(self.tokens)
        self.w1 = dict()
        self.w2 = dict()
        self.calcScore()
        self.ranked_w1 = sorted(self.w1.items(), key=operator.itemgetter(1), reverse=True)
        self.ranked_w2 = sorted(self.w2.items(), key=operator.itemgetter(1), reverse=True)

        
    def calcScore(self):
        for doc in self.docs:
            w1 = 0
            w2 = 0
            for token in self.tokens:
                w1 += self.calcW1(token, doc)
                w2 += self.calcW2(token, doc)
            self.w1[doc] = w1
            self.w2[doc] = w2



    def calcW1(self, token, doc):
        if get_df(token) == 0:
            return 0
        tf = get_tf(token, doc)
        maxtf = get_maxtf(doc)
        df = get_df(token)
        cs = get_collectionsize()
        term1 = log(0.5 + tf)/log(maxtf+1.0)
        term1 = 0.4 + (0.6*term1) 
        term2 = log(cs/df)/log(cs)
        return term1*term2

    def calcW2(self,token, doc):
        if get_df(token) == 0:
            return 0
        tf = get_tf(token, doc)
        df = get_df(token)
        doclen = get_doclen(doc)
        avgdoclen = get_avgdoclen()
        cs = get_collectionsize()

        term1 = tf + 0.5 + (1.5*doclen/avgdoclen)
        term1 = tf/term1
        term2 = log(cs/df)/log(cs)
        term = 0.4 + (0.6*term1*term2)
        return term

    # Get the union of all the documents for a query
    def get_docs(self, tokens):
        docList = set()
        for word in tokens:
            docs = get_docList(word)
            docList |= set(docs)
        return docList

    def parse(self, query):
        
        """
        This method returns the list of stemmed tokens from the query.

        """

        words = query.split()
        result = []

        for word in words:
            r = self.clean(word)
            if r:
                result.append(stem(r))
        return result

    def clean(self, token):
        if token.startswith('<') and token.endswith('>'):
            return 0

        if token.isalpha():
            if len(token) <= 1:
                return 0
            if token in stop_words:
                return 0
            return token
            
        str_to_replace = [',', "'s", '.', '-', '(',')' ]
        for s in str_to_replace:
            token = token.replace(s,'')

        if token.isdigit() or not token.isalpha():
            return 0

        if len(token) <= 1:
            return 0

        if token in stop_words:
            return 0
        
        return token


    
