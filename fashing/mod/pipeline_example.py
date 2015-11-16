#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import nltk

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities
from gensim.models import Word2Vec
from nltk.corpus import brown, words, wordnet

# Create Dictionary
path = '/tmp/'
fashion_words = []

# read data file and put every json into an array
with open("../../data/plain_text.json", "r") as text_file:
    text = text_file.readlines()

with open("../../data/fashion-words.txt", "r") as text_file:
    f_words = text_file.readlines()

for word in f_words:
    for dic in word.lower().split():
        fashion_words.append([dic.strip('[],')[1:-1]])

# Example plain texts 
plain_text_doc_1 = "just shot the lookbook for Canadian outerwear brand Northern Sun. the company was established in the seventies, and quickly became synonymous with finely crafted, Canadian-made jackets and parkas that stand up to the demands of an unforgiving climate."
plain_text_doc_2 = "It's been a while since my last blog post...please do forgive me but I have one terribly unfashionable word for you: CRUTCHES! ugh. Anyhoo, I'll try to work in OOTD posts here and there but right now my wardrobe consists of easy to pull on sweats and that's hardly interesting. So, back to businesss!"
documents = [plain_text_doc_1, plain_text_doc_2]

# stuff we need later on
tokens = []
list_of_words = []

# NLTK: tokenizing and appending tokens to list of words
for document in documents:
    sentences = nltk.sent_tokenize(document)
    for s in sentences:
        tok_words = nltk.word_tokenize(s.lower())

        for word in tok_words:
            list_of_words.append(word)

list_of_words = list_of_words

# Testing models for Word2Vec:

model_1 = Word2Vec(brown.sents())
#model_2 = Word2Vec(words.words()) #kP
print "################################################################################################################"
print "#                              Words from dictionary with hightes Similarity                                   #"
print "################################################################################################################"

sim = 0
word = ""

for w in list_of_words:
    for f in fashion_words:
        try:
            cos = model_1.similarity(w, f[0])
            if cos > sim:
                sim = cos
                word = f[0]
        except:
            pass
    print w + " --> " + word + " | similarity: " + str(sim)
    sim = 0

print "################################################################################################################"
print "#                                Top 5 similar words from Word2Vec corpus brown                                #"
print "################################################################################################################"

for w in list_of_words:
    try:
        print w + ": " + str(model_1.most_similar(w, topn=5))
    except:
        print (w + " is not in vocabulary!")


print "################################################################################################################"

#print model_1.similarity("woman", "man")
#print words.words()
#print wordnet


