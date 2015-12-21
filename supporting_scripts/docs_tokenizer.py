#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
import pprint
import nltk
from os.path import join
import os

PROJECT_DIR = os.path.dirname(__file__) + "/../"

with open(PROJECT_DIR + "data/example_docs.json", "r") as text_file:
  text = json.load(text_file)

with open(PROJECT_DIR + "data/example_docs_tokenized.json", "a") as example_docs_tags:
    example_docs_tags.seek(0)
    example_docs_tags.truncate()


def nltk_tokenizing(document):
  number_of_documents = 0
  max_documents = 50
  # number_of_documents = 0
  #
  # NLTK Tokenizing
  #

  # for x in range(0, 1):
  # reads first json
  # json_data = json.loads(document)
  x = 0
  for data in document:
    print(x)
    x += 1
    print(data)
    extracted_text = data["extracted_text"]
    sentences = nltk.sent_tokenize(extracted_text)

    entities = []
    indicies = []

    for s in sentences:
      for word in (nltk.tag.pos_tag(nltk.word_tokenize(s))):
        if word[1] == "NN" or word[1] == "NNP" or word[1] == "NNPS" or word[1] == "NNS":
          i_tmp = []
          for m in re.finditer(word[0], extracted_text):
            i_tmp.append([m.start(), m.end()])

            entities.append(word[0].encode('utf-8'))
            indicies.append(i_tmp)

    tmp = {"_id": data["_id"]["$oid"], "entities": entities, "indicies": indicies}

    pre = ""
    suf = ""

    if number_of_documents == 0:
      pre = "["
      suf = ","
    elif number_of_documents == max_documents - 1:
      suf = "]"
    else:
      suf = ","

    number_of_documents += 1

    if number_of_documents == max_documents:
      break

    with open(PROJECT_DIR + "data/example_docs_tokenized.json", "a") as example_docs_tags:
      example_docs_tags.writelines(pre + json.dumps(tmp).encode('utf-8') + suf + "\n")


nltk_tokenizing(text)
