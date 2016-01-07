#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import pickle
import nltk
import json
import os
import sys
from gensim.models import Word2Vec

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# read data file and put every json into an array
with open("../../data/input_data/plain_text_optimized_eng.json", "r") as text_file:
  text = text_file.readlines()

with open("../../data/fashion-words.txt", "r") as text_file:
  f_words = text_file.readlines()

token_file = open("../../data/dictionaries/token_words.txt", "w")

length = len(text)

for doc in text:
  # reads first json
  json_data = json.loads(doc)

  # print(json_data)
  extracted_text = json_data["extracted_text"]
  sentences = nltk.sent_tokenize(extracted_text)

  # nltk version 3.1 beacuse in 3.0 pos_tag doesnt work
  # tokenize sentences and add nouns to array
  tokens = []
  for s in sentences:
    s.lower()
    s = nltk.word_tokenize(s)
    tokens.append(s)
    #pickle.dump(s, token_file)

  pickle.dump(tokens, token_file)
  if ( text.index(doc) % 1000 == 0 ):
    print str(text.index(doc)) + " of " + str(length) + " sentences tokenized"

class MySentence(object):

  def __iter__(self):
  #Pickle streams are entirely self-contained,
  # and so unpickling will unpickle one object at a time
    while 1:
     try:
        p = pickle.load(token_file)
        for l in p:
          yield l

     except EOFError:
         break

token_file = open("../../data/dictionaries/token_words.txt", "r")
sentences = MySentence()
model = Word2Vec([doc for doc in sentences])
model.save('../../data/models/fashion_model')

