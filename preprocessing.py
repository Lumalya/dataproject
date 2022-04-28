#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################### Libraries ####################

import extraction  # import the module extraction.py
import nltk
import spacy
import string
from nltk.corpus import stopwords
import pandas as pd

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
    Return the list of tokens without the stopwords
    """
    
    # init var
    output_tokens = []
    
    # core
    for token in input_tokens:          # parsing the list of tokens
        if token not in en_stopwords:   # if the token is not a stopword
            output_tokens.append(token) # adding into the output list
    return output_tokens



def extract_people(input_text):
    """list(spacy_string) -> list(spacy_string)
    Return the list of people extracted from the input_text
    """
    
    # init var
    output_people = []
    
    # core
    for ent in input_text.ents:         # parsing the input_text
        if ent.label_ == 'PERSON':      # checking if the token is a person
            output_people.append(ent)   # adding it to the output lists
    return output_people



def add_article(df, person, page_text, page_preprocessed, desc, desc_preprocessed):
    """DataFrame(spacy_string * 5) * spacy_string * 5 -> pd.DataFrame(spacy_string * 5)
    Hypothesis : It only work for one article
    Return the dataframe with 5 columns containing the input information
    """
    
    # core
    df2 = pd.DataFrame([[person,
                         page_text,
                         page_preprocessed,
                         desc,
                         desc_preprocessed]], columns = df.index.name)
    df.append(df2)
    return df



#def POS_tagging():
#    pass



#def named_entity_recognition():
#    pass



def create_database(extracted_data):
    """list(spacy_string) -> DataFrame(spacy_string * 5)
    Create a dataframe then row add_article to add content from extracted data
    """
    
    # var init
    
    df = pd.DataFrame(columns = ["person",
                                 "Wikipedia page text",
                                 "Wikipedia page text after preprocessing",
                                 "Wikidata description"
                                 "Wikidata description after preprocessing"])
    
    # core
        # Preprocessing the extracted data
        
    for content in ...:         # parsing all the data extracted, preprocessed
        
        person = ...
        page_text = ...
        page_preprocessed = ...
        desc = ...
        desc_preprocessed = ...
        
        df = add_article(df, person, page_text, page_preprocessed, desc, desc_preprocessed)
    
    return df    
    

#################### Test ####################