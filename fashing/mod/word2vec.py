#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import nltk
import json
import os
import sys

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities
from pprint import pprint

# Create Dictionary
path = '/tmp/'

# read data file and put every json into an array
with open("../../../data/plain_text.json", "r") as text_file:
  text = text_file.readlines()

with open("../../../data/fashion-words.txt", "r") as text_file:
  f_words = text_file.readlines()

# Example document
documents = ["sandal with jacket dress vest tuxedo",
             "brief gown here is what you",
             "sandal without jacket",
             "to brief a person",
             "tuxedo"]

tokens = []
token = 0
data = []
nouns = []
test = []

print(f_words)
for word in f_words:
  for dic in word.lower().split():
    print(dic)
    test.append([dic.strip('[],')[1:-1]])

for document in documents:
  # for x in range(0, 1):
  # reads first json
  # json_data = json.loads(text[x])

  # print(json_data)
  # extracted_text = json_data["extracted_text"]
  sentences = nltk.sent_tokenize(document)

  # nltk version 3.1 beacuse in 3.0 pos_tag doesnt work
  # tokenize sentences and add nouns to array
  for s in sentences:
    s.lower()
    tokens.append(nltk.word_tokenize(s))
    words_with_tags = nltk.tag.pos_tag(nltk.word_tokenize(s))

    for w in words_with_tags:
      if w[1] == "NN" or w[1] == "NNP" or w[1] == "NNPS" or w[1] == "NNS":
        nouns.append(w[0])

  data.append(nouns)

######create dictionary with unique tokens
######array of tokens with nouns from nltk
dictionary = corpora.Dictionary(data)
print(dictionary.token2id)
dictionary.save(path + 'zalando.dict')

######match dict with documents
corpus = [dictionary.doc2bow(text) for text in tokens]
corpora.MmCorpus.serialize(path + 'zalando.mm', corpus)
# corpus = corpora.MmCorpus('/tmp/zalando.mm')

# print(nouns)
# print(tokens)
# print(dictionary)
print (corpus)

#####Similarity Interface############
####doc should be dictionary with fashion words
docs = test
lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)
vec_bow = [dictionary.doc2bow(doc) for doc in docs]

vec_lsi = lsi[vec_bow]
print(vec_lsi)

######Similarity Query######
index = similarities.MatrixSimilarity(lsi[corpus])
index.save(path + 'zalando.index')
index = similarities.MatrixSimilarity.load(path + 'zalando.index')
sims = index[vec_lsi]
# sims = sorted(enumerate(sims), key=lambda item: -item[1])
print(sims)
