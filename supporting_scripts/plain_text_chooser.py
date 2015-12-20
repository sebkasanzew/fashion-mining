#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re

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
taging = []

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


    tmp = {"_id" : json_data["_id"], "entities": entities, "indicies": indicies}

    if number_of_entities >= 2:
        number_of_documents+=1

        with open("../data/example_docs.json", "a") as example_docs:
            example_docs.writelines(str(json_data) + "\n")
        with open("../data/example_docs_tags.json", "a") as example_docs_tags:
            example_docs_tags.writelines(str(tmp) + "\n")
        print json_data
        print tmp

    if number_of_documents == 50:
        break
