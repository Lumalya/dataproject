#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################### Libraries ####################

import pandas as pd
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Perceptron # notre modèle à appliquer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report



#################### Global ####################

random_state = 59

#################### Functions ####################

def convert_cat_to_idx(category):

    # core
    return cat_to_idx[category]



def rebuild_sentence(words):
    
    # core
    return ' '.join(words)



def show_scores(Y_test, Y_pred, idx_to_cat):
    
    # core
    for i in range(15):
        print(i, idx_to_cat[i])
    
    print('Accuracy:', accuracy_score(Y_test, Y_pred))
    print(confusion_matrix(Y_test, Y_pred))
    print(classification_report(Y_test, Y_pred))



def show_accuracy(Y_test, Y_pred):
    '''
    How many time there is the good result
    '''
    
    # init var
    categories = []
    
    # core
    for i in range(15):
        categories.append(idx_to_cat[i])
    
    accuracies = confusion_matrix(Y_test, Y_pred, normalize = "true").diagonal()
    scores = {'Categories': categories, 'Accuracy': accuracies}
    df_scores = pd.DataFrame(scores)
    
    plot = df_scores.plot.bar(title = 'Score per category', x = 'Categories')
    plot.set_ylim([0, 1.1])
    plot.set_xlabel('Category')
    plot.set_ylabel('Accuracy')
    #plot.set_xticklabels(categories, rotation = 90)
    


#################### Test ####################

df = pd.read_csv('DataSet.csv') # put back in file
df = shuffle(df, random_state=random_state)

all_categories = df['categories'].unique()
cat_to_idx = {}
idx_to_cat = {}

for i, cat in enumerate(all_categories):
    cat_to_idx[cat] = i
    idx_to_cat[i] = cat

df['category_index'] = df['categories'].apply(convert_cat_to_idx)

Y = df['category_index']

# creating word as number
vectorizer = TfidfVectorizer(max_features = 400, 
                             use_idf = True, 
                             stop_words = 'english'
                             )

X = vectorizer.fit_transform(df['preprocessed_texts']) # .astype(str) and maybe .apply(rebuild_sentence)
print(X)

# separate into train and test set
X_train, X_test, Y_train, Y_test = train_test_split(X, 
                                                    Y, 
                                                    test_size = 0.25, 
                                                    random_state=random_state
                                                    )

# creating classifier
perceptron = Perceptron()
perceptron.fit(X_train, Y_train) # train by fitting the data into the model
Y_pred = perceptron.predict(X_test)
print('kkkk')

print('Predictions:') # predicted values 
for pred in Y_pred:
    print(str(pred).ljust(3), end = '')
print()

print('Expected:') # real values
for pred in Y_test:
    print(str(pred).ljust(3), end=  '')
print()

show_scores(Y_test, Y_pred, idx_to_cat)
# show_accuracy(Y_test, Y_pred)

# Show most important words for each category
# It influence the model to choose this category
tag_to_idx = dict(vectorizer.vocabulary_)
idx_to_tag = {v: k for k, v in tag_to_idx.items()}

coeffs = perceptron.coef_.transpose()

weights = {i: coeffs[i] for i in range(len(coeffs))}

for class_num, class_weights in enumerate(perceptron.coef_):
    print(idx_to_cat[class_num])
    print()
    top_vals = sorted(enumerate(class_weights), reverse = True, key = lambda x: x[1])
    for id, val in top_vals[:6]:
        print(idx_to_tag[id], val)
    print()
    print()
 