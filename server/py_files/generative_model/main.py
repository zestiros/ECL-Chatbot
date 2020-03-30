# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 19:50:13 2020

@author: ruiya
"""

from __future__ import unicode_literals, print_function, division

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
import copy
import sys
sys.path.append('C://Users//ruiya//Desktop//projet_ecl//generative_model')

from models import *
from utils import *
from training import *



def beam_search(encoder,decoder,input_lang,output_lang,sentence,beam_size,max_length = MAX_LENGTH,stem=False):
    sentence = unicodeToAscii(sentence)
    if stem:
        sentence=stemString(sentence,stemmer)
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

    decoder_output, decoder_hidden, decoder_attention = decoder(
        decoder_input, decoder_hidden, encoder_outputs)

    topv,topi = decoder_output.data.topk(beam_size)

    new_decoder_hidden = decoder_hidden.expand(beam_size,*decoder_hidden.size())

    prevs_words = torch.zeros(beam_size*beam_size,MAX_LENGTH)


    prevs_words[:,0] = SOS_token
    scores = torch.zeros(beam_size*beam_size)
    output_sentence = []
    out_scores = []
    step = 1
    for i in range(beam_size):
        scores[i*beam_size:(i+1)*beam_size] = topv[0][i]
        prevs_words[i*beam_size:(i+1)*beam_size,1] = topi[0][i].item()
        
    while(len(out_scores)<beam_size and step<20):
        for i in range (beam_size):
            decoder_input = Variable(torch.LongTensor([[prevs_words[i*beam_size,step]]]))
            decoder_hidden = new_decoder_hidden[i]
            decoder_output, decoder_hidden, decoder_attention = decoder(
            decoder_input, decoder_hidden, encoder_outputs)
            topv,topi = decoder_output.data.topk(beam_size)
            new_decoder_hidden[i] = decoder_hidden
            for j in range(beam_size):
                prevs_words[j+i*beam_size,step+1] = topi[0][j].item()

                scores[j+i*beam_size] +=topv[0][j]



        s_topv,s_topi = scores.topk(beam_size)    
       # print(scores)
        #print(s_topi)
        prevs_words_copy = copy.deepcopy(prevs_words)
        new_decoder_hidden_copy = torch.zeros(*new_decoder_hidden.size())
        for i in range(beam_size):
            scores[i*beam_size:(i+1)*beam_size] = s_topv[i]
            prevs_words[i*beam_size:(i+1)*beam_size,:] = prevs_words_copy[s_topi[i],:]
            new_decoder_hidden_copy[i] = new_decoder_hidden[s_topi[i]//beam_size]
        new_decoder_hidden = new_decoder_hidden_copy
        for i in range(beam_size):
            if prevs_words[i*beam_size,step+1]==EOS_token and scores[i*beam_size].item()>-100:
               # print(prevs_words[i*beam_size,:],scores[i*beam_size])
                a = prevs_words[i*beam_size,:].numpy()
                b = copy.deepcopy(a)
                output_sentence.append(b)
                #print(output_sentence)
                out_scores.append(scores[i*beam_size].item())
                scores[i*beam_size:(i+1)*beam_size] = -500


        #print(step)     
        step+=1
    answer = ''
    out_sentence = output_sentence[out_scores.index(max(out_scores))]
    for i in out_sentence:
        token = output_lang.index2word[i.item()]
        if token == "EOS":
            break
        if token !="SOS":
            answer = answer + ' ' + token
   # print("question : {}\n".format(sentence))
    print(answer)
    return answer


if __name__=='__main__':
    # define path
    dirname =os.path.dirname(__file__)
    DATA_FILE = os.path.join(dirname,'../data/data.txt')
    # ENCODER_FILE1 = os.path.join(dirname,'../no_stem_checkpoints/encoder20000_para.pkl') #no use stemming
    ENCODER_FILE2 = os.path.join(dirname,'../stem_checkpoints/encoder_35000_stem_ns_para.pkl') #use stemming
    # DECODER_FILE1 = os.path.join(dirname,'../no_stem_checkpoints/decoder20000_para.pkl') # no use stemming
    DECODER_FILE2 = os.path.join(dirname,'../stem_checkpoints/decoder_35000_stem_ns_para.pkl') #use stemming
 #prepare data
    SOS_token = 0
    EOS_token = 1
    MAX_LENGTH = 25
    input_lang_stem, output_lang_stem, pairs_stem = prepareData('questions', 'answers',DATA_FILE, False,stem=True)
    new_sentence = "je ne comprend pas"
    output_lang_stem.addSentence(new_sentence)
    new_sentence = stemString(new_sentence,stemmer)
    new_sentence = normalizeString(new_sentence)
    #new_sentence = stemString(new_sentence)
    new_sentence = TrimWordsSentence(new_sentence)
    # print(new_sentence)
    input_lang_stem.addSentence(new_sentence)
    
#define model    
    hidden_size = 256
    encoder_stem = EncoderRNN(input_lang_stem.n_words, hidden_size,n_layers=1)
    decoder_stem = AttnDecoderRNN(hidden_size, output_lang_stem.n_words,n_layers=1, dropout_p=0.1)
    
#load model    
    encoder_stem.load_state_dict(torch.load(ENCODER_FILE2))
    decoder_stem.load_state_dict(torch.load(DECODER_FILE2))

# chat
    # q1 = " combien de cours du mth tc1 ?"
    # beam_search(encoder_stem,decoder_stem,input_lang_stem,output_lang_stem,q1,beam_size=3,max_length = MAX_LENGTH,stem=True)
    # chat(encoder_stem,decoder_stem,input_lang_stem,output_lang_stem,q1,stem=True)

#node server
    text_from_node_server = str(sys.argv[1])
    # beam_search(encoder_stem,decoder_stem,input_lang_stem,output_lang_stem,text_from_node_server,beam_size=3,max_length = MAX_LENGTH,stem=True)
    chat(encoder_stem,decoder_stem,input_lang_stem,output_lang_stem,text_from_node_server,stem=True)

    sys.stdout.flush()