# -*- coding: utf-8 -*-

import json
import nltk

print("This is a Test for NLTK!")

### read data file and put every json into an array
with open("data/plain_text.json", "r") as text_file:
    text = text_file.readlines()
# print(text[0])

### reads first json
json_test = json.loads(text[0])
extracted_text = json_test["extracted_text"]

#Sentence Tokenization
sentences = nltk.sent_tokenize(extracted_text)

#Word Tokenization
for s in sentences:
    words = nltk.word_tokenize(s)
    print words
    # Part of Speech Tagging
    print(nltk.tag.pos_tag(words))


