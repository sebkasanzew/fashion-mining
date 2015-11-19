#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import nltk

with open("../data/plain_text_2.json", "r") as text_file:
    text = text_file.readlines()

data = []
int = 0

for x in text:
    # reads first json
    json_data = json.loads(x)

    extracted_text = json_data["extracted_text"]

    sentences = nltk.sent_tokenize(extracted_text)
    # print(sentences)

    # Sentence Tokenizing
    for s in sentences:
        data.append(nltk.word_tokenize(s))

    print int
    int += 1

with open('../data/plain_text_corpus_2.txt', 'w') as outfile:
    json.dump(data, outfile)
