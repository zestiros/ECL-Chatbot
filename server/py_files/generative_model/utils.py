# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 19:35:30 2020

@author: ruiya
"""
from io import open
import unicodedata
import string
import re
import random
import numpy as np
import os

import torch
import torch.nn as nn
from torch.autograd import Variable
from torch import optim
import torch.nn.functional as F
from nltk.stem.snowball import FrenchStemmer
stemmer = FrenchStemmer()
SOS_token = 0
EOS_token = 1
class Lang:
    def __init__(self, name):
        self.name = name
        self.word2index = {"Null" :2}
        self.word2count = {}#count the frenquence of a word appear in the document
        self.index2word = {0: "SOS", 1: "EOS", 2:"Null"} # SOS : start of sentence; EOS: end of sentence; 
        # Null : word doesn't exist in the traning data.
        self.n_words = 3  # Count SOS and EOS and Null

    def addSentence(self, sentence):
        ''' add  a sentence to the class'''
        for word in sentence.split():
            if word == '':
                print('****************',sentence)
            self.addWord(word)
         
    def addWord(self, word):
        ''' add a word to the class '''
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1

# Turn a Unicode string to plain ASCII, thanks to
# http://stackoverflow.com/a/518232/2809427
def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

# Lowercase, trim, and remove non-letter characters except digits
def normalizeString(s):
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"(['\'()/&!{}\-\’])", r" ", s)
    #s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    #s = re.sub(r"[^a-zA-Z0-9?]+", r" ", s)
    #s = re.sub(r"[^a-zA-Z0-9?&\'\’\%\-]+", r" ", s)
    #s = re.sub(r"[^a-zA-Z0-9?&\%\-]+", r" ", s)
    return s

def readLangs(questions, answers,DATA_FILE, reverse=False,stem=False):
    # print("Reading lines...")
        
    lines = open(DATA_FILE, encoding='utf-8').\
        read().strip().split('\n')
    # Split every line into pairs and normalize
    pairs = [[s for s in l.split('\t')] for l in lines]
    if stem:
        for pair in pairs:
            pair[0] = stemString(pair[0],stemmer)
            pair[0] = normalizeString(pair[0])
            pair[1] = normalizeString(pair[1])
    else : 
        for pair in pairs:
            pair[0] = normalizeString(pair[0])
            pair[1] = normalizeString(pair[1])
            
    # Reverse pairs, make Lang instances
    if reverse:
        pairs = [list(reversed(p)) for p in pairs]
        input_lang = Lang(answers)
        output_lang = Lang(questions)
    else:
        input_lang = Lang(questions)
        output_lang = Lang(answers)

    return input_lang, output_lang, pairs


MAX_LENGTH = 25
# we use stopwords to delete those words not meaningfull
stopwords = 'de du des d le la les l ce c ci ça m me ma si t sur n en s si a y au un une on il nous vous je j a b c d e r f avoir'.split()

#stopwords = []

def TrimWordsSentence(sentence):
    resultwords = [word for word in sentence.split() if word.lower() not in stopwords]
    resultwords = ' '.join(resultwords)
    return resultwords

def TrimWords(pairs):
    for pair in pairs: 
        pair[0] = TrimWordsSentence(pair[0])
        pair[1] = TrimWordsSentence(pair[1])
    return pairs

# delete longer sentences
def filterPair(p):
    return len(p[0].split()) < MAX_LENGTH and \
        len(p[1].split()) < MAX_LENGTH 

def filterPairs(pairs):
    return [pair for pair in pairs if filterPair(pair)]

def prepareData(lang1, lang2, DATA_FILE,reverse=False,stem=False):
    input_lang, output_lang, pairs = readLangs(lang1, lang2,DATA_FILE, reverse,stem)
    # print("Read %s sentence pairs" % len(pairs))
    pairs = TrimWords(pairs)
    
    # for pair in [pair for pair in pairs if not filterPair(pair)]:
    #     print('%s (%d) -> %s (%d)' % (pair[0],len(pair[0].split()),pair[1],len(pair[1].split())))  
    
    pairs = filterPairs(pairs)
    
    # print('')
    # print("Trimmed to %s sentence pairs" % len(pairs))
    # print("Counting words...")
    for pair in pairs:
        input_lang.addSentence(pair[0])
        output_lang.addSentence(pair[1])
        if '' in output_lang.word2index: print(pair[1].split())
    # print("Counted words:")
    # print(input_lang.name, input_lang.n_words)
    # print(output_lang.name, output_lang.n_words)
    return input_lang, output_lang, pairs


def indexesFromSentence(lang, sentence,MAX_LENGTH=25):
    words = sentence.split()
    if len(words)>MAX_LENGTH:
        new_words = random.choices(words,k=MAX_LENGTH)
    else:
        new_words = words
    
    
    a = []
    for word in new_words:
        try:
            a.append(lang.word2index[word])
        except KeyError:
            a.append(lang.word2index['Null'])
    
    return a

def variableFromSentence(lang, sentence):
    indexes = indexesFromSentence(lang, sentence)
    indexes.append(EOS_token)
    result = Variable(torch.LongTensor(indexes).view(-1, 1))
    return result

def variablesFromPair(input_lang,output_lang,pair):
    input_variable = variableFromSentence(input_lang, pair[0])
    target_variable = variableFromSentence(output_lang, pair[1])
    return (input_variable, target_variable)

def stemString(s,stemmer):
    
    new_str = ""
    for i in s.split(' '):
        new_str = new_str + " " + stemmer.stem(i)
  
    return new_str
def evaluate(encoder, decoder, input_lang,output_lang,sentence, max_length=25,stem=False):
    sentence = unicodeToAscii(sentence)
    if stem:
        sentence = stemString(sentence,stemmer)
    sentence = normalizeString(sentence)
    sentence = TrimWordsSentence(sentence)
    input_variable = variableFromSentence(input_lang, sentence)
    input_length = input_variable.size()[0]
    encoder_hidden = encoder.initHidden()

    encoder_outputs = Variable(torch.zeros(max_length, encoder.hidden_size))

    for ei in range(input_length):
        encoder_output, encoder_hidden = encoder(input_variable[ei],
                                                 encoder_hidden)
        encoder_outputs[ei] = encoder_outputs[ei] + encoder_output[0][0]

    decoder_input = Variable(torch.LongTensor([[SOS_token]]))  # SOS

    decoder_hidden = encoder_hidden

    decoded_words = []
    decoder_attentions = torch.zeros(max_length, max_length)

    for di in range(max_length):
        
        #decoder_output, decoder_hidden = decoder(
         #   decoder_input, decoder_hidden)

        decoder_output, decoder_hidden, decoder_attention = decoder(
            decoder_input, decoder_hidden, encoder_outputs)
        decoder_attentions[di] = decoder_attention.data

        topv, topi = decoder_output.data.topk(1)
        ni = topi[0][0].item()

        if ni == EOS_token:
            decoded_words.append('<EOS>')
            break
        else:
            decoded_words.append(output_lang.index2word[ni])

        decoder_input = Variable(torch.LongTensor([[ni]]))
    # print("norm_question : {}".format(sentence))
    return decoded_words, decoder_attentions[:di + 1]
    #return decoded_words
    
def evaluateRandomly(encoder, decoder,input_lang,output_lang, n=10,stem=False):
    for i in range(n):
        pair = random.choice(pairs)
        print('>', pair[0])
        print('=', pair[1])
        
        output_words, attentions = evaluate(encoder, decoder,input_lang,output_lang, pair[0],stem=stem)
        #output_words = evaluate(encoder, decoder, pair[0])
     
        output_sentence = ' '.join(output_words)
        print('<', output_sentence)
        print('')
        
def showAttention(input_sentence, output_words, attentions):
    # Set up figure with colorbar
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(attentions.numpy(), cmap='bone')
    fig.colorbar(cax)

    # Set up axes
    ax.set_xticklabels([''] + input_sentence.split(' ') +
                       ['<EOS>'], rotation=90)
    ax.set_yticklabels([''] + output_words)

    # Show label at every tick
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

    plt.show()

def evaluateAndShowAttention(input_sentence,encoder1,attn_decoder1,input_lang,output_lang):
    output_words, attentions = evaluate(
        encoder1, attn_decoder1,input_lang,output_lang,input_sentence)
    showAttention(input_sentence, output_words, attentions)

def Norm(ques):
    if ques[-1] =="?":
        ques = ques[0:-1]+" ?"
    return ques

def chat(encoder,decoder,input_lang,output_lang,sentence,stem=False):
    sentence = Norm(sentence)
    answer = ''
    for i in evaluate(encoder,decoder,input_lang,output_lang,sentence,stem=stem)[0] :
        if i == "<EOS>":
            break
        answer = answer + ' ' + i
    # print("question : {}\n".format(sentence))
    print(answer)