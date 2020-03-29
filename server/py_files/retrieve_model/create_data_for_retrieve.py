# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 19:27:41 2020

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

def create_data(filename):
    doc = open('{}//{}'.format(raw_data_path,filename),encoding='utf-8').read().strip()
    lines = re.split('\n\n\n\d+\n',doc)
    pages = []
    page_number = re.findall('\n\n\n\d+\n',doc)
    for i in range(len(page_number)):
        page_number[i] = re.findall('\d+',page_number[i])[0]
    page_number.append("{}".format(int(page_number[-1])+1))

    for i in lines:
        if i!="":
            pages.append(i)
    for page in range(len(pages)):
        with open("{}/{}_page{}.txt".format(DATA_FILE_retrieve,filename.split('.txt')[0],page_number[page]), "w",encoding='utf-8') as text_file:
            text_file.write(pages[page])


if __name__=='__main__':
    dirname = "C://Users//ruiya//Desktop//projet_ecl"
    raw_data_path = os.path.join(dirname,'scolarite_raw_data')
    raw_files = os.listdir(raw_data_path)
    DATA_FILE_retrieve = os.path.join(dirname,'retrieve_data//')
    for filename in raw_files:
        if re.search('.txt',filename)!=None:
            create_data(filename)