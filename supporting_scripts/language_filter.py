#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords

with open("../data/plain_text_optimized.json", "r") as text_file:
    docs = text_file.readlines()

def _calculate_languages_ratios(text):
    languages_ratios = {}

    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]

    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)

        languages_ratios[language] = len(common_elements)

    return languages_ratios

def detect_language(text):
    ratios = _calculate_languages_ratios(text)
    most_rated_language = max(ratios, key=ratios.get)
    return most_rated_language

def filtering_file(file):

    l = len(file)
    i = 0

    with open("../data/plain_text_optimized_2.json.json", "a") as myfile:
        myfile.seek(0)
        myfile.truncate()

        for line in file:
            print str(i) + "/" + str(l)
            i+=1

            data = json.loads(line)
            text = data["extracted_text"]

            if detect_language(text) == "english":
                    myfile.write(line)

if __name__=='__main__':
    filtering_file(docs)

