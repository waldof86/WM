# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 10:45:18 2020

@author: Marcos Buccellato
"""

#  Importing libraries and module and some setting for name matching 
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from scipy.sparse import csr_matrix
import sparse_dot_topn.sparse_dot_topn as ct  # Leading Juice for us

import pandas as pd

def ngrams(string, n=3):
    string = re.sub(r'[,-./]|\sBD',r'', string)
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]
def awesome_cossim_top(A, B, ntop, lower_bound=0):
    # force A and B as a CSR matrix.
    # If they have already been CSR, there is no overhead
    A = A.tocsr()
    B = B.tocsr()
    M, _ = A.shape
    _, N = B.shape
 
    idx_dtype = np.int32
 
    nnz_max = M*ntop
 
    indptr = np.zeros(M+1, dtype=idx_dtype)
    indices = np.zeros(nnz_max, dtype=idx_dtype)
    data = np.zeros(nnz_max, dtype=A.dtype)
    ct.sparse_dot_topn(
        M, N, np.asarray(A.indptr, dtype=idx_dtype),
        np.asarray(A.indices, dtype=idx_dtype),
        A.data,
        np.asarray(B.indptr, dtype=idx_dtype),
        np.asarray(B.indices, dtype=idx_dtype),
        B.data,
        ntop,
        lower_bound,
        indptr, indices, data)
    return csr_matrix((data,indices,indptr),shape=(M,N))

# unpacks the resulting sparse matrix
def get_matches_df(sparse_matrix, name_vector, top=100):
    non_zeros = sparse_matrix.nonzero()
    
    sparserows = non_zeros[0]
    sparsecols = non_zeros[1]
    
    if top:
        nr_matches = top
    else:
        nr_matches = sparsecols.size
    
    left_side = np.empty([nr_matches], dtype=object)
    right_side = np.empty([nr_matches], dtype=object)
    similairity = np.zeros(nr_matches)
    
    for index in range(0, nr_matches):
        left_side[index] = name_vector[sparserows[index]]
        right_side[index] = name_vector[sparsecols[index]]
        similairity[index] = sparse_matrix.data[index]
    
    return pd.DataFrame({'left_side': left_side,
                          'right_side': right_side,
                           'similairity': similairity})

def find_nearest_match(data,pres,limit=1) :
        vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams)
        tf_idf_matrix = vectorizer.fit_transform(data)
        #  similarity above 0.8
        matches = awesome_cossim_top(tf_idf_matrix, tf_idf_matrix.transpose(), len(data), pres)
        matches_df = get_matches_df(matches, data, top=len(data))
        matches_df = matches_df[matches_df['similairity'] < 0.99999] # For removing all exact matches
        #matches_df = matches_df[matches_df['left_side'] == data[0]] 
        return matches_df[:limit]


def synonym_sustitution(dic,wrd,pres=5):        
    import Levenshtein

    dic['distance'] = dic.apply(lambda x: Levenshtein.distance(x['Palabra'], wrd),axis=1)
    dic = dic[dic['distance'] < pres]
    if not dic.empty:
        return dic.iloc[dic['distance'].argmin()][1]
    else:
        return wrd


inst_clean = ["Universidad de Buenos Aires","Instituto de Buenos Aires", "Universal de Buenos Aires", "UADE school of business", "IAE school of business"]
wrd = "IAE escua de negocios"
syn_dict  = pd.read_csv("Institutions.csv") 

res = synonym_sustitution(syn_dict,wrd,5)

#inst_clean.insert(0,wrd)
#documents=inst_clean
#print(find_nearest_match(inst_clean,0.01,1))
