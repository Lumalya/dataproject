#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################### Libraries ####################

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.utils import shuffle #clustering algorithm on some data using N clusters
from sklearn import metrics # a function to compute evaluation scores for clustering results
import nltk
import pandas as pd

import preprocessing # import the module preprocessing.py

#################### Functions ####################

def train_clustering(data, n_clusters):
    '''
    Return a kmeans clustering model
    '''
    
    # core
    km = KMeans(n_clusters = n_clusters)
                    # Apply the clustering model on the tf-idf matrix (the features)
    km.fit(data)    # applying model on data
    return km



def compute_scores(km, categories, tfidf):
    '''
    Return the scores
    '''
    
    # core
    homogeneity = metrics.homogeneity_score(categories, km.labels_)
    completeness = metrics.completeness_score(categories, km.labels_)
    v_measure = metrics.v_measure_score(categories, km.labels_)
    rand_index = metrics.adjusted_rand_score(categories, km.labels_)
    silhouette = metrics.silhouette_score(tfidf, km.labels_, sample_size = 1000)
    
    print("Homogeneity: %0.3f" % homogeneity) # km.labels_ = clusters obtenus
    print("Completeness: %0.3f" % completeness)
    print("V-measure: %0.3f" % v_measure)
    print("Adjusted Rand-Index: %.3f" % rand_index)
    print("Silhouette Coefficient: %0.3f" % silhouette)

    scores = {} # mise dans dico
    scores['homogeneity'] = homogeneity
    scores['completeness'] = completeness
    scores['v_measure'] = v_measure
    scores['rand_index'] = rand_index
    scores['silhouette'] = silhouette

    return scores



def visualize_metrics(df, tfidf):
    '''
    Plot those metrics values for values of N ranging from 2 to 16
    '''
    
    # init var
    all_scores = [] # empty list to calc all scores one by one
    for n_clusters in range(2, 17): # train with 2 to 16 clusters
        km = train_clustering(tfidf, n_clusters)
        scores = compute_scores(km, df['category'], tfidf)
        all_scores.append(scores)

    df = pd.DataFrame(all_scores) # df containing all scores
    df.index = range(2, 17) # 2 to 16 clusters
    plot = df.plot.line(title = 'Scores de clustering')
    plot.set_xlabel('Nombre de clusters')
    plot.set_ylabel('Scores')



def rebuild_sentence(words):
    return ' '.join(words)



#################### Test ####################

df = pd.read_json('test')
df = shuffle(df)

df['output_text'] = df['output_text'].apply(rebuild_sentence)
corpus = df['output_text']

vectorizer = TfidfVectorizer(max_features = 500, #number of token which we want to know frequency
                             use_idf = True,
                             stop_words = 'english',
                             tokenizer = nltk.word_tokenize)

tfidf = vectorizer.fit_transform(corpus) # freq of words in a corpus

visualize_metrics(df, tfidf)
