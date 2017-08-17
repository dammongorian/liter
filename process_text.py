from __future__ import division
import urllib2
import re
import lxml.html
from datetime import datetime
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import string
import nltk, re, pprint
from nltk import word_tokenize

def clean_story(raw_story):
    # takes a string and performs several pre-processing steps for LDA
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords.extend(["n't","'s","''","``","--",'...',"'re","'m","'d","'ve",'would','woman','man','dick','cock','pussy','cunt','hand','one','two','as','get','said','thought','like'])
    punc = string.punctuation
    lemma = WordNetLemmatizer()
    p_stemmer = PorterStemmer()
    
    tokens = word_tokenize(raw_story)
    tagged = nltk.tag.pos_tag(tokens)
    non_nnp = [word.lower() for word,tag in tagged if tag != 'NNP' and tag != 'NNPS']

    content = [word for word in non_nnp if word not in stopwords and word not in punc]
    lemmad = [lemma.lemmatize(word) for word in content]
    
    return lemmad