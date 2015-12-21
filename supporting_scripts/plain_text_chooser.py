#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
import pprint

with open("../data/plain_text_optimized_eng_filtered.json", "r") as text_file:
    docs = json.load(text_file)

with open("../data/entities.txt", "r") as text_file:
    dict = text_file.readlines()

with open("../data/example_docs.json", "a") as example_docs:
    example_docs.seek(0)
    example_docs.truncate()

with open("../data/example_docs_tags.json", "a") as example_docs_tags:
    example_docs_tags.seek(0)
    example_docs_tags.truncate()

dict = eval(dict[0])
number_of_documents = 0
max_documents = 50

for doc in docs:
    number_of_entities = 0

    text = doc["extracted_text"].replace('\n',' ')
    doc["extracted_text"] = text

    entities = []
    indicies = []

    for entity in dict:
        if entity in text:
            number_of_entities += 1
            i_tmp = []

            contains = False;
            for m in re.finditer(entity, text):
                if not text[m.start()-1].isalpha() and not text[m.end()].isalpha():
                    contains = True
                    i_tmp.append([m.start(), m.end()])



            if contains:
                entities.append(entity.encode("utf-8"))
                indicies.append(i_tmp)

    tmp = {"_id" : doc["_id"]["$oid"], "entities": entities, "indicies": indicies}

    pre = ""
    suf = ""
    if number_of_entities >= 2:
        if number_of_documents == 0:
            pre = "["
            suf = ","
        elif number_of_documents == max_documents-1:
            pre = ""
            suf = "]"
        else:
            suf = ","

        number_of_documents += 1

        with open("../data/example_docs.json", "a") as example_docs:
            example_docs.writelines(pre + str(json.dumps(doc)) + suf + "\n")
        with open("../data/example_docs_tags.json", "a") as example_docs_tags:
            example_docs_tags.writelines(pre + str(json.dumps(tmp)) + suf + "\n")
        #print json_data
        #print tmp

    if number_of_documents == max_documents:
        break