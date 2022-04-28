#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################### Libraries ####################

import extraction  # import the module extraction.py
import nltk
import spacy
import string
from nltk.corpus import stopwords
import pandas

#################### Init ####################

nltk.download('stopwords')                  # initializing stopwords
en_stopwords = stopwords.words('english')   # generating the list of stopwords

#################### Functions ####################

def text_to_sent(input_text):
    """spacy_string -> list(spacy_string)
    Return the list of sentences from an input_text
    """
    # core
    return input_text.sents



def text_to_token(input_text):
    """list(spacy_string) -> list(spacy_string)
    Return the list of tokens from an input_text
    """
    # init var
    output_tokens = []
    
    # core
    for word in input_text:                 # parsing all the sentences
        output_tokens.append(word.text)     # tokenize and put in the output list
    return output_tokens



def punct_lower(input_tokens):
    """list(spacy_string) -> list(spacy_string)
    Return the same word by lowering and removing punctuation
    """

    # init var    
    output_tokens = []
    
    # core
    # making a table of translation using str.maketrans(before:string, after:string, remove:string)
    table = str.maketrans(string.ascii_uppercase, string.ascii_lowercase, string.punctuation)
    
    for token in input_tokens:              # parsing all token
        new_token = token.translate(table)  # apply the replacement to one token
        output_tokens.append(new_token)     # adding the new token in the list
    return output_tokens



def remove_stopwords(input_tokens):
    """list(spacy_string) -> list(spacy_string)
    Returning the list of tokens without the stopwords
    """
    
    # init var
    output_tokens = []
    
    # core
    for token in input_tokens:          # parsing the list of tokens
        if token not in en_stopwords:   # if the token is not a stopword
            output_tokens.append(token) # adding into the output list
    return output_tokens



def create_dataframe(input_data):
    """
    
    """
    
#################### Test ####################
