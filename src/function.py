import pandas as pd
import joblib
import re
import numpy as np
import datetime
import pyrebase
import firebase_admin

from firebase_admin import credentials
from firebase_admin import db
from pythainlp.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfTransformer


def main(chat_text):
    model = joblib.load('asset/text_clf.sav')
    corpus = joblib.load('asset/corpus.sav')
    cus_dict = joblib.load('asset/cus_dict.sav')

    # Fetch the service account key JSON file contents
    cred = credentials.Certificate('line-bot-chrins-firebase-adminsdk.json')

    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://line-bot-chrins.firebaseio.com'
    })
    ref = db.reference("/")

    money = int(re.findall("[0-9]+", text)[0])
    expression = r"(.*?)[0-9]"
    t = re.findall(expression, text)[0].replace(' ', '')

    tmp = get_BOW([text], corpus, cus_dict)
    label = labeling(model.predict(tmp))

    # saving data
    # create date
    d = datetime.datetime.today().strftime("%Y/%m/%d")
    # create data to push
    data = {"Date": d, "money": money, "text": t, 'type': label}
    ref.push(data)

    return


def get_BOW(text, corpus, trie, tfidf=True):
    BOW = [list() for i in range(len(text))]
    l = 0
    count = 1
    for i in text:
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

    BOW = np.array(BOW)

    if tfidf:
        tfidf_transformer = TfidfTransformer()
        return tfidf_transformer.fit_transform(BOW)
    else:
        return BOW


def labeling(code):
    if code == 0:
        return 'Income'
    elif code == 1:
        return 'Expenses'
