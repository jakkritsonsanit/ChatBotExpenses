import pandas as pd
import numpy as np
from pythainlp.corpus.common import thai_words
from pythainlp.tokenize import dict_trie, word_tokenize
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.model_selection import cross_val_score

def train():
    df = pd.read_csv("Data/Expenses.csv")

    custom_dict = set(thai_words())
    word = ['ราเมง', 'อิเกีย', 'คาปูชิโน่', 'น้ำมัน','หอยลาย', 'ปุ้มปุ้ย']
    for i in word:
        custom_dict.add(i)
    trie = dict_trie(dict_source=custom_dict)

    corpus = []
    for i in df.text:
        for j in word_tokenize(i, engine='dict', custom_dict=trie):
            if j not in corpus:
                corpus.append(j)

    BOW = [list() for i in range(len(df.text))]
    l = 0
    count = 1
    for i in df.text:
        tmp = word_tokenize(i, engine='dict', custom_dict=trie)
        for j in corpus:

            if j in tmp:

                BOW[l].append(tmp.count(j))
                tmp.remove(j)
                
            else:
                BOW[l].append(0)
            
        if len(tmp) != 0:
            BOW[l].append(len(tmp))
        elif len(tmp) == 0:
            BOW[l].append(0)
        l += 1

    ytarget = df.cate
    xtrain = BOW

    dtree = DecisionTreeClassifier()
    dtree.fit(X=xtrain,y=ytarget)

    return corpus, dtree


def createBOW(ls_txt, corpus):

    custom_dict = set(thai_words())
    word = ['ราเมง', 'อิเกีย', 'คาปูชิโน่', 'น้ำมัน','หอยลาย', 'ปุ้มปุ้ย']
    for i in word:
        custom_dict.add(i)
    trie = dict_trie(dict_source=custom_dict)

    BOW_t = [list() for i in range(len(ls_txt))]
    l = 0
    for i in ls_txt:
        tmp = word_tokenize(i, engine='dict', custom_dict=trie)
        for j in corpus:

            if j in tmp:

                BOW_t[l].append(tmp.count(j))
                tmp.remove(j)
            else:
                BOW_t[l].append(0)
            
        if len(tmp) != 0:
            BOW_t[l].append(len(tmp))
        elif len(tmp) == 0:
            BOW_t[l].append(0)
        l += 1

    # corpus_t = corpus.append('Other')
    # ch = pd.DataFrame({
    #     'train':corpus,
    #     'target':BOW_t[0]
    # })
    # ch
    # predictiontree = dtree.predict(BOW_t)
    return list(BOW_t)



