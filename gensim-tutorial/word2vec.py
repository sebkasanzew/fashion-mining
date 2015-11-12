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
path = '/tmp/zalando.dict'

# if os.path.exists(path) == False:
#     print('create dictionary')
#     data = [[word.strip('[],')[1:-1] for word in tempList.split()] for tempList in open("../dict.txt", "r")]
#     dictionary = corpora.Dictionary(data)
#     dictionary.save(path)
#     print(dictionary)
# else:
#   dictionary = corpora.Dictionary.load(path)


#print(dictionary.token2id)
#Example document
documents = [ "sandal with jacket dress vest tuxedo",
             "brief gown here is what you",
              "sandal without jacket",
              "to brief a person",
              "tuxedo"]

tokens = []
token = 0
data = []
nouns = []
for document in documents:
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
dictionary.save(path)

######match dict with documents
corpus = [dictionary.doc2bow(text) for text in tokens]
corpora.MmCorpus.serialize('/tmp/zalando.mm', corpus)
#corpus = corpora.MmCorpus('/tmp/zalando.mm')

# print(nouns)
# print(tokens)
# print(dictionary)
# print (corpus)


#####Similarity Interface############
####doc should be dictionary with fashion words
doc = "tuxedo"
lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow]
print(vec_lsi)


######Similarity Query######
index = similarities.MatrixSimilarity(lsi[corpus])
index.save('/tmp/zalando.index')
index = similarities.MatrixSimilarity.load('/tmp/zalando.index')
sims = index[vec_lsi]
sims = sorted(enumerate(sims), key=lambda item: -item[1])
print(sims)


