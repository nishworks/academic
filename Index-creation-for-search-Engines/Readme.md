Index Creation for search engines


This project generate inverted indexes which are referred by search engines to return results.
It  builds two versions of the index for a simple statistical retrieval system and also each version
of the index in uncompressed form and compressed form.Version 1 of index considers the terms in the
dictionary to be lemmas of words, whereas version 2 of index considers that the terms of the dictionary
are stems of the tokens.Before building the dictionaries of any of the two versions of index, stop words
are removed from the dictionaries. These stop words are listed in stopwords file.

Stemmer : Porter stemmer

For every term that is both versions of the indexed, store:
- Document frequency (df): The number of documents that the term occurs in
- Term frequency (tf):     The number of times that the term occurs in each document
- The list of documents containing the term

Compression : Gamma and delta encoding is used for compression

To execute : 

	python create_index.py path_to_dir

        path_to_dir - Directory containting the documents


Dependicies:
	
	Python 2.7+
	NLTK
	NLTK Data - Wordnet and maxent treebank POS Tagger
	bitarray (pypi)
	bitstring (pypi)

Output:

	Four Index files
    		Index_Version1
    		Index_Version1.compressed
    		Index_Version2
    		Index_Version2.compressed

