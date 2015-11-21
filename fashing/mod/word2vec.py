#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import nltk
import json
import os
import sys
import gensim
import texttable as tt
from gensim import corpora, models, similarities
from pprint import pprint

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def main():
  """The main test executable"""
  # Here goes the code from below
  # Create Dictionary


  path = '/tmp/'

  # read data file and put every json into an array
  with open("../../data/plain_text.json", "r") as text_file:
    text = text_file.readlines()

  with open("../../data/fashion-words.txt", "r") as text_file:
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

  print(data)
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


  # #####Similarity Interface############
  # ####doc should be dictionary with fashion words
  # docs = test
  # lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)
  # vec_bow = [dictionary.doc2bow(doc) for doc in docs]
  #
  # vec_lsi = lsi[vec_bow]
  # print(vec_lsi)
  #
  # ######Similarity Query######
  # index = similarities.MatrixSimilarity(lsi[corpus])
  # index.save(path + 'zalando.index')
  # index = similarities.MatrixSimilarity.load(path + 'zalando.index')
  # sims = index[vec_lsi]
  # # sims = sorted(enumerate(sims), key=lambda item: -item[1])
  # print(sims)


def word2vec():
  with open("../../data/plain_text.json", "r") as text_file:
    text = text_file.readlines()

  with open("../../data/fashion-words.txt", "r") as text_file:
    f_words = text_file.readlines()

  fashion_words = []
  for word in f_words:
    for dic in word.lower().split():
      fashion_words.append([dic.strip('[],')[1:-1]])

  # NLTK Tokenizing
  tokens = []
  list_of_words = []
  for x in range(0, 3):
    # reads first json
    json_data = json.loads(text[x])

    # print(json_data)
    extracted_text = json_data["extracted_text"]

    # Sentence Tokenizing
    sentences = nltk.sent_tokenize(extracted_text)
    # print(sentences)
    for s in sentences:
      # Word tokenizing and tagging
      tok_words = nltk.word_tokenize(s)
      for word in tok_words:
        list_of_words.append(word)

  #print "################################################################################################################"
  #print "#                              Words from dictionary with highest similarity                                   #"
  #print "################################################################################################################"

  # load model for word2vec
  model_1 = gensim.models.Word2Vec.load('../../data/models/fashion_model')

  sim = 0
  word = ""
  tab_array = []
  row_array = []

  for w in list_of_words:
    # appending Word
    row_array.append(str(w))
    #TODO: appending POS-Tag
    row_array.append("--")
    try:
      #print w
      top_three = model_1.most_similar(w, topn=3)

      #print top_three

      row_array.append(str(top_three[0][0]))
      row_array.append(round(top_three[0][1], 4))
      #print(top_three[0][0])
      #print(round(top_three[0][1], 4))

      row_array.append(str(top_three[1][0]))
      row_array.append(round(top_three[1][1], 4))
      #print(top_three[1][0])
      #print(round(top_three[1][1], 4))

      row_array.append(str(top_three[2][0]))
      row_array.append(round(top_three[2][1], 4))
      #print(top_three[0][0] + " | " + top_three[1][0] + " | " + top_three[2][0])
      #print(round(top_three[2][1], 4))

    except:
      #print(row_array)
      for x in range(0, 6):
        row_array.append("**")
        #print (w + " is not in vocabulary!")

    for f in fashion_words:
      try:
        cos = model_1.similarity(w, f[0])
        # cos = model_1.similarity("/en/" + w, "/en/" + f[0])
        if cos > sim:
          sim = cos
          word = f[0]
      except:
        pass

    sim = 0
    #appending JOIN-Partner
    row_array.append(str(word))
    #print w + " --> " + word + " | similarity: " + str(sim)

    #print row_array
    #add row to tab_array, reset row
    tab_array.append(row_array)
    row_array = []


  # Creating a test Table
  tab = tt.Texttable()
  tab.header(['Words', 'POS-Tag', 'Word1', 'Cos-Dist', 'Word2', 'Cos-Dist', 'Word3', 'Cos-Dist', 'JOIN-Partner'])

  for row in tab_array:
    #print row
    #TODO Fix bug
    if len(row) == 9:
      tab.add_row(row)


  #tab.add_row(['Zalando', 'NN', 'H&M',	'0,6434', 'word2',	'0,6234', 'word3', '0,5324', 'shoe'])
  #tab.add_row(['is', 'VB', 'word2',	'0,6434', 'word2',	'0,6234', 'word3', '0,5324', 'blub'])
  #tab.add_row(['big', 'AD', 'word2',	'0,6434', 'word2',	'0,6234', 'word3', '0,5324', 'fubar'])

  tab.set_cols_width([15,15,15,15,15,15,15,15,15])
  tab.set_cols_align(['l','l','l','l','l','l','l','l','l'])
  tab.set_cols_valign(['t','t','t','t','t','t','t','t','t'])
  tab.set_deco(tab.HEADER | tab.VLINES)
  tab.set_chars(['-','|','+','#'])

  print "##########################################     TEST     ########################################################"
  print
  print tab.draw()
  print
  print "################################################################################################################"


def custom_public_function_reachable_from_outside():
  """define functions that can be accessed from main.py and other modules"""


if __name__ == "__main__":
  # Execute the main function if this file was executed from the terminal
  word2vec()
