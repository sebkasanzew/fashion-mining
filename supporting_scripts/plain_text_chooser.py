#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
import pprint

with open("../data/plain_text_optimized_eng_filtered.json", "r") as text_file:
    docs = text_file.readlines()

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
indicies_data = []
example_data = []

for doc in docs:
    number_of_entities = 0

    json_data = json.loads(doc)
    text = json_data["extracted_text"]

    entities = []
    indicies = []

    for entity in dict:
        if entity in text:
            number_of_entities += 1
            i_tmp = []

            for m in re.finditer(entity, text):
                i_tmp.append([m.start(), m.end()])

            entities.append(str(entity))
            indicies.append(i_tmp)

    tmp = {"_id" : json_data["_id"]["$oid"], "entities": entities, "indicies": indicies}

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


        number_of_documents+=1
        indicies_data.append(tmp)
        example_data.append(json.dumps(json_data))

        with open("../data/example_docs.json", "a") as example_docs:
            example_docs.writelines(pre + str(json.dumps(json_data)) + suf + "\n")
        with open("../data/example_docs_tags.json", "a") as example_docs_tags:
            example_docs_tags.writelines(pre + str(json.dumps(tmp)) + suf + "\n")
        #print json_data
        #print tmp

    if number_of_documents == max_documents:
        break