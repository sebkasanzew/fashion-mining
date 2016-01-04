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
from os.path import join
import numpy as np

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Global Paths TODO: improvement of dirs
PROJECT_DIR = os.path.dirname(__file__) + "/../../"
GLOVE_DIR = PROJECT_DIR + "data/tmp/"

#TODO: refactor code which draws the table
def word2vec():
    """
    executes the main logic of word2vec
    :return: result-json with tagged words, indices and cosine distance
    """
    # Loading external files
    with open(PROJECT_DIR + "data/example_docs_tokenized.json", "r") as text_file:
        text = json.load(text_file)
    with open(PROJECT_DIR + "data/one_word_entities_reduced.txt", "r") as text_file:
        fashion_dictionary = text_file.readlines()
    with open(PROJECT_DIR + "data/vector_words_tags.json", "a") as vector_words:
        vector_words.seek(0)
        vector_words.truncate()
    #with open(PROJECT_DIR + "data/fashion-words.txt", "r") as text_file:
    #    fashion_dictionary = text_file.readlines()


    # read words from fashion dictionary
    fashion_words = []
    for word in fashion_dictionary:
        for dic in word.lower().split():
            fashion_words.append([dic.strip('[],')[1:-1]])

    # load model for word2vec
    model = load_model(1)

    number_of_documents = 0
    max_documents = 50
    sim = 0

    for doc in text:
        cos_dist = []
        extracted_tokens = doc["entities"]
        for token in extracted_tokens:
            for f in fashion_words:
                try:
                    # cos = model.similarity("/en/" + w[0], "/en/" + f[0])
                    cos = model.similarity(token.lower(), f[0].lower())
                    if cos > sim:
                        sim = cos
                        word = f[0]
                except:
                    pass

            # appending JOIN-Partner
            if sim == 0:
                cos_dist.append(["NONE", "NONE"])
            else:
                cos_dist.append([str(word), str(sim)])
                sim = 0

        doc["cosDist"] = cos_dist

        pre = ""
        if number_of_documents == 0:
            pre = "["
            suf = ","
        elif number_of_documents == max_documents - 1:
            suf = "]"
        else:
            suf = ","
            # list_of_words.append(token)

        number_of_documents += 1

        with open(PROJECT_DIR + "data/vector_words_tags.json", "a") as example_docs_tags:
            example_docs_tags.writelines(pre + json.dumps(doc).encode('utf-8') + suf + "\n")

        if number_of_documents == max_documents:
            break

    ###########################################################################################
    # sim = 0
    # word = ""
    #
    # data = []
    #
    # tab_array = []
    # row_array = []
    #
    # counter = 0
    # for w in list_of_words:
    #   data.append([])
    #   data[counter].append(w)
    #
    #   # appending Word
    #   row_array.append(w.encode("utf-8"))
    #   # appending POS-Tag
    #   row_array.append(w.encode("utf-8"))
    #
    #   try:
    #     # appending top three words
    #     top_three = model.most_similar(w, topn=3)
    #     data[counter].append(top_three)
    #
    #     row_array.append(str(top_three[0][0]))
    #     row_array.append(round(top_three[0][1], 4))
    #     row_array.append(str(top_three[1][0]))
    #     row_array.append(round(top_three[1][1], 4))
    #     row_array.append(str(top_three[2][0]))
    #     row_array.append(round(top_three[2][1], 4))
    #
    #   except:
    #     try:
    #       len(data[counter][1])
    #     except:
    #       data[counter].append([("-----", "-----"), ("-----", "-----"), ("-----", "-----")])
    #
    #     for x in range(0, 8 - len(row_array)):
    #       # print (w + " is not in vocabulary!")
    #       row_array.append("-----")
    #
    #   for f in fashion_words:
    #     try:
    #       # cos = model.similarity("/en/" + w[0], "/en/" + f[0])
    #       cos = model.similarity(w.lower(), f[0].lower())
    #       if cos > sim:
    #         sim = cos
    #         word = f[0]
    #     except:
    #       pass
    #
    #   # appending JOIN-Partner
    #   if sim == 0:
    #     data[counter].append("NONE")
    #     row_array.append("NONE")
    #   else:
    #     data[counter].append(str(word) + "\n" + str(sim))
    #     row_array.append(str(word) + "\n" + str(sim))
    #
    #     sim = 0
    #
    #
    #
    #   # add row to tab_array, reset row
    #   tab_array.append(row_array)
    #
    #   counter += 1
    #   row_array = []

    print
    print "###########################################################################################################################"
    print "#                                            Textmining with Word2Vec and NLTK                                            #"
    print "###########################################################################################################################"

    # tab_array = collect_table_data(data)
    # draw_table(tab_array)

    print "Returning auto tagged json..."
    with open(PROJECT_DIR + "data/vector_words_tags.json", "r") as text_file:
        result = json.load(text_file)
    return result

def nltk_tokenizing(document):
    """
    Takes a JSON-Document, which contains plaintext at key "extracted_text" and returns a list of single words
    after tokenizing with NLTK
    :param document:
    :return: list of words
    """
    #
    # NLTK Tokenizing
    #
    list_of_words = []

    for data in document:
        print(data)
        extracted_text = data["extracted_text"]
        sentences = nltk.sent_tokenize(extracted_text)

        for s in sentences:
            for word in (nltk.tag.pos_tag(nltk.word_tokenize(s))):
                if word[1] == "NN" or word[1] == "NNP" or word[1] == "NNPS" or word[1] == "NNS":
                    list_of_words.append(word)
    return list_of_words


def load_model(x):
    """
    loads a model which depends on the given parameter:
    0: Glove Model
    1: Own Fashion Model created from Zalando Documents
    :param x: integer
    :return: path of model
    """
    if x == 0:
        '''
        Convert Glove Model to Gensim Word2Vec
        GloVe is another algorithm that creates vector representations of words similar to word2vec.
        GloVe transforms the neutral network problem into a word co-occurrence matrix so it should
        be faster to train but uses more memory.
        '''

        def any2unicode(text, encoding='utf8', errors='strict'):
            if isinstance(text, unicode):
                return text
            return unicode(text.replace('\xc2\x85', '<newline>'), encoding, errors=errors)

        gensim.models.utils.to_unicode = any2unicode

        return gensim.models.Word2Vec.load_word2vec_format(join(GLOVE_DIR, 'common.840B.300d.txt'), binary=False)

    if x == 1:
        return gensim.models.Word2Vec.load(PROJECT_DIR + 'data/models/fashion_model')

    #if x == 2:
    #    return gensim.models.Word2Vec.load_word2vec_format('/opt/word2vec/freebase_model_en.bin.gz', binary=True)

# TODO collecting table data
def collect_table_data(data):
    result = []
    row_array = []

    for line in data:
        # row_array.append(line[0][0])
        # row_array.append(line[0][1])
        # row_array.append(str(line[1][0][0]).encode('utf8'))
        # row_array.append(str(line[1][0][1]))
        # row_array.append(str(line[1][1][0]).encode('utf8'))
        # row_array.append(str(line[1][1][1]))
        # row_array.append(str(line[1][2][0]).encode('utf8'))
        # row_array.append(str(line[1][2][1]))
        # row_array.append(line[2])
        # result.append(row_array)
        row_array = []

    return result


# draws a table
def draw_table(tab_array):
    tab = tt.Texttable()
    tab.header(['Words', 'POS-Tag', 'Word1', 'Cos-Dist', 'Word2', 'Cos-Dist', 'Word3', 'Cos-Dist', 'JOIN-Partner'])

    for row in tab_array:
        tab.add_row(row)

    # tab.add_row(['Zalando', 'NN', 'H&M',	'0,6434', 'word2',	'0,6234', 'word3', '0,5324', 'shoe'])
    # tab.add_row(['is', 'VB', 'word2',	'0,6434', 'word2',	'0,6234', 'word3', '0,5324', 'blub'])
    # tab.add_row(['big', 'AD', 'word2',	'0,6434', 'word2',	'0,6234', 'word3', '0,5324', 'fubar'])

    tab.set_cols_width([15, 5, 15, 5, 15, 5, 15, 5, 15])
    tab.set_cols_align(['l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l'])
    tab.set_chars(['-', '|', '+', '='])

    print tab.draw()


def custom_public_function_reachable_from_outside():
    """define functions that can be accessed from main.py and other modules"""


if __name__ == "__main__":
    # Execute the main function if this file was executed from the terminal
    word2vec()
