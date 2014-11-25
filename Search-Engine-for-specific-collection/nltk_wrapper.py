#!usr/bin/env python
#-*-coding:utf8-*-
__doc__ = """
This module acts as a wrapper over nltk module.
This exposes just the methods we need in a programmer
friendly way.

Dependecies : nltk, numpy,nltk-data
    nltk-data : wordnet
        Use NLTK Downloader to download.
        You can do this by running 
        import nltk 
        nltk.download()
             Models/maxent_treebank_pos_tagger.
             corpora/wordnet
        Download location in mac/unix : /usr/share/nltk_data
"""
import nltk
import nltk.stem.wordnet as wordnet
from nltk.stem.porter import PorterStemmer

_lemmatizer = wordnet.WordNetLemmatizer().lemmatize

def _wordnet_pos_tag(word):
    tag = nltk.pos_tag([word])[0][1]
    if tag.startswith('NN'):
        return wordnet.wordnet.NOUN
    elif tag.startswith('VB'):
        return wordnet.wordnet.VERB
    elif tag.startswith('JJ'):
        return wordnet.wordnet.ADJ
    elif tag.startswith('RB'):
        return wordnet.wordnet.ADV
    else:
        return ''

# Exposed methods
stem = PorterStemmer().stem

def lemma_of(word):
    tag = _wordnet_pos_tag(word)
    if tag == '':
        tag = wordnet.wordnet.NOUN

    return _lemmatizer(word, tag)