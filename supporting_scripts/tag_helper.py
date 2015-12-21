#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re

with open("../data/example_docs_tags_manuell.json", "r") as text_file:
    tags_man = json.load(text_file)

with open("../data/example_docs.json", "r") as text_file:
    docs = json.load(text_file)

with open("../data/example_docs_tags_manuell_final.json", "a") as clear:
    clear.seek(0)
    clear.truncate()

#for doc in docs:
#    print doc["extracted_text"]

counter = 0

for data in tags_man:
    indicies = []

    if docs[counter]["extracted_text"] == []:
        text = [""]
    else:
        text = docs[counter]["extracted_text"]

    if len(data["entities"]) != 0:

        for x in range (0, len(data["entities"])):
            #print data["entities"][x]
            i_tmp = []
            for m in re.finditer(data["entities"][x], text):
                i_tmp.append([m.start(), m.end()])
            indicies.append(i_tmp)

        data["indicies"] = indicies

    else:
        data["indicies"] = [[[0, 0]]]

    counter +=1

with open("../data/example_docs_tags_manuell_final.json", "a") as example_docs:
    example_docs.writelines(json.dumps(tags_man)+ "\n")