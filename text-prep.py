# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 14:29:33 2021

@author: Marcos Buccellato
"""
#import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer


# Gensim
import gensim
import gensim.corpora as corpora
from gensim.models import CoherenceModel


#other imports
import string
import re
import numpy as np
import pandas as pd


#Cargo datos
df_clarin = pd.read_excel (r'clarin-results.xlsx')
df_lanacion = pd.read_excel (r'lanacion-results.xlsx')
#df_full = pd.concat([df_clarin, df_lanacion], axis=0)
#df_full.reset_index()
df_full = df_lanacion
doc_complete = df_full['artículo']

###Topic Modeling

###FIRST https://www.analyticsvidhya.com/blog/2016/08/beginners-guide-to-topic-modeling-in-python/

stop = set(stopwords.words('spanish'))
#stop.extend(['from', 'subject', 're', 'edu', 'use'])

exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

doc_clean = [clean(doc).split() for doc in doc_complete]  


#TOPIC MODELING

# Creating the term dictionary of our courpus, where every unique term is assigned an index. dictionary = corpora.Dictionary(doc_clean)
dictionary = corpora.Dictionary(doc_clean)

# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

# Running and Trainign LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=8, id2word = dictionary, passes=50)

print(ldamodel.print_topics(num_topics=8, num_words=3))


########

#### Topic clasification