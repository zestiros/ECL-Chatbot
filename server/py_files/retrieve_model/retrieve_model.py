# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 19:17:59 2020

@author: ruiya
"""

import nltk
import numpy as np
import random
import string
from io import open
import unicodedata
import re
import random
import os
from nltk.stem.snowball import FrenchStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import copy
import sys

nltk.download('punkt')




def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

def normalizeString(s):
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"([^a-zA-Z0-9'\'()/&!{}\-\’||,◊:.])", r" ", s)
    #s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    #s = re.sub(r"[^a-zA-Z0-9?]+", r" ", s)
    #s = re.sub(r"[^a-zA-Z0-9?&\'\’\%\-]+", r" ", s)
    #s = re.sub(r"[^a-zA-Z0-9?&\%\-]+", r" ", s)
    return s

stopwords = 'de du des d le la les l ce c ci ça m me ma si t sur n en s si a y au un une on il nous vous je j a b c d e r f avoir '.split()


def TrimWordsSentence(sentence):
    resultwords = [word for word in sentence.split() if word.lower() not in stopwords]
    resultwords = ' '.join(resultwords)
    return resultwords

def LemNormalize(doc):
    doc = stemString(doc,stemmer)
    doc = unicodeToAscii(doc)
    doc = normalizeString(doc)
    doc = TrimWordsSentence(doc)
    words = nltk.word_tokenize(doc)
    return words

def key_search(question,all_doc,match_dict):
    new_doc = copy.deepcopy(all_doc)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize)
    new_doc.append(question)
    tfidf = TfidfVec.fit_transform(new_doc)
    vals = cosine_similarity(tfidf[-1],tfidf)
    ind = vals.argsort()[0][-4:-1]
    for i in ind:
        answer = match_dict["{}".format(i)]
        doc_site = match_dict["{}".format(answer.split("_")[0])]
        print("{}{}".format(doc_site,answer.split("_")[-1].split(".")[0]))
    return ind



def stemString(s,stemmer):
    new_str = ""
    for i in s.split(' '):
        new_str = new_str + " " + stemmer.stem(i)
    return new_str




if __name__ == '__main__':
    
    dirname = os.path.dirname(__file__)

    raw_data_path = os.path.join(dirname,'scolarite_raw_data')
    raw_files = os.listdir(raw_data_path)
    DATA_FILE_retrieve = os.path.join(dirname,'retrieve_data/')
    stemmer = FrenchStemmer()
    
    files = os.listdir(DATA_FILE_retrieve)

    match_dict = {}
    all_doc = []
    i = 0
    for file in files:  
        doc = open('{}/{}'.format(DATA_FILE_retrieve,file), encoding='utf-8').read().strip()
        match_dict["{}".format(i)] = file
        all_doc.append(doc)
        i +=1
    match_dict['ueS5'] = "https://drive.google.com/open?id=1zwQMGZFFG2fUhMiEJB3aiPMjXAQJ7lhq"
    match_dict['s9Metier'] = "https://drive.google.com/file/d/1LQsF2iglGQDk-bPyf9rLkc4x1OiW7sJi/view?usp=sharing"
    match_dict['s9MOD'] = 'https://drive.google.com/file/d/1u9DSAcBjBPVEzSXk2rFSM8UscLZia_3R/view?usp=sharing'
    match_dict['s9Secteur'] = 'https://drive.google.com/file/d/1nqUI1ywgBYQSFvAubbvWQXSJ7GVezgXB/view?usp=sharing'
    match_dict['ueS7'] = 'https://drive.google.com/file/d/1Gr3XwKbMf0BtoaYGo3kSDyvqOiRMZFG_/view?usp=sharing'
    match_dict['ueS8'] = 'https://drive.google.com/file/d/1KmAPKqaSta_6HD9CbR7DzGY7c5n93Cvm/view?usp=sharing'
    match_dict['noteECS'] = 'https://drive.google.com/file/d/12tQD0N0KoWKOF4Cw7p57_rH7f1u49ZPJ/view?usp=sharing'
    match_dict['noteFLE'] = 'https://drive.google.com/file/d/1-N7oRoBba5wyRS0kS_D5xvX78B5DYog_/view?usp=sharing'
    match_dict['noteGM'] = 'https://drive.google.com/file/d/1SUsvI79fMeaJ_mguUQ6xI0KQm6Z4tDcv/view?usp=sharing'
    match_dict['noteIDM'] = 'https://drive.google.com/file/d/1pstkqUQrl4vk9eiDAZIq0cC--lONlJpR/view?usp=sharing'
    
#node server
    text_from_node_server = str(sys.argv[1])

    val = key_search(text_from_node_server,all_doc,match_dict)

    sys.stdout.flush()

