#!usr/bin/env python
#-*-coding:utf8-*-
__doc__ = """
This module has the classes which provied the filesystem
related classes and methods.
It has following global attributes :
    stop_words              : List of stop words going to be used in program
"""
import os
import sys
import re

stop_words = []
#Calulate stop words
with open('stopwords', 'r') as file:
    for line in file:
        stop_words.append(line[:-1].strip())

class Directory():

    """This class represents the directory object with following attributes :

        Path       : Path of the directory
        no_of_docs : Number of docs in the directory
        docs_list  : Generator object that has list of docpaths

    """

    __slots__ = ['Path','__list_of_docs', 'no_of_docs','docs_list']

    def __init__(self,path):
        self.Path = path
        self.__list_of_docs = [ os.path.join(self.Path, filename) \
                                    for filename in os.listdir(self.Path) \
                                        if os.path.isfile(os.path.join(self.Path, filename))]
        
        #usable attributes
        self.no_of_docs = len(self.__list_of_docs)
        #Iterator
        self.docs_list = self.__listDocs()

    def __listDocs(self):
        for filePath in self.__list_of_docs:
            yield filePath

class Doc():

    """
    Attributes explained as follows:

    Path          :   Path to the file including filename
    doclen        :   Number of tokens in file including stop words
    docid         :   Integer value at the end of filename
                      Example : filename = "Cranfield0021" docid = 21
    tokens        :   List of words in file

    """

    __slots__ = ['Path','doclen', 'docid','tokens']


    def __init__(self,path):
        self.Path = path
        self.docid = int(re.findall("(\d+)$",self.Path)[0])
        self.doclen = 0
        self.__tokens = []
        self.tokenize()
        self.tokens = self.__iterToken()

    def tokenize(self):
        with open(self.Path, 'r') as file:
            for line in file:
                words = line.split()
                for word in words:
                    self.clean_and_register(word.lower().strip())

    def __iterToken(self):
        for t in self.__tokens:
            yield t

    
    def clean_and_register(self,token):
        
        if token.startswith('<') and token.endswith('>'):
            return

        if token.isalpha():
            self.doclen += 1
            if len(token) <= 1:
                return
            if token in stop_words:
                return
            self.__tokens.append(token)
            return

        str_to_replace = [',', "'s", '.', '-', '(',')' ]
        for s in str_to_replace:
            token = token.replace(s,'')
 
        if token.isdigit() or not token.isalpha():
            return

        if len(token) <= 1:
            return

        self.doclen += 1

        if token in stop_words:
            return

        self.__tokens.append(token)

