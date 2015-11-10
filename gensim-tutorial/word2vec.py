#!/usr/bin/python
# coding: utf-8

import logging;
import nltk;
import os;
import sys;

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO);

# from nltk import pos_tag, word_tokenize, sent_tokenize
from gensim import corpora, models, similarities
from pprint import pprint

# Create Dictionary
path = '/tmp/deerwester.dict'

if os.path.exists(path) == False:
    print('create dictionary')
    data = [[word.strip('[],')[1:-1] for word in tempList.split()] for tempList in open("../dict.txt", "r")]
    dictionary = corpora.Dictionary(data)
    dictionary.save(path)
    print(dictionary)
else:
  dictionary = corpora.Dictionary.load(path)


print(dictionary.token2id)
#Example document
documents = [ "sandal with jacket dress vest tuxedo",
             "brief gown" ]

tokens = []
token = 0
test = []
for document in documents:
  sentences = nltk.sent_tokenize(document)

# nltk version 3.1 beacuse in 3.0 pos_tag doesnt work

  for s in sentences:
    token = nltk.word_tokenize(s)
    print(token)
    tokens.append(nltk.word_tokenize(s))

  test.append(dictionary.doc2bow(token))


print(test)
