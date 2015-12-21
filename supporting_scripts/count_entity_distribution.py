#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import csv

with open("../data/example_docs.json", "r") as text_file:
    docs = json.load(text_file)

with open("../data/entities.txt", "r") as text_file:
    dict = eval(text_file.readlines()[0])

counted_entities = {}

c = 0
l = len(docs)
for doc in docs:
    c+=1
    print str(c) + " / " + str(l)

    text = doc["extracted_text"]

    for entity in dict:
        if entity in text:

            if entity in counted_entities.keys():
                counted_entities[entity] = counted_entities[entity] + 1
            else:
                counted_entities[entity] = 1

sorted_entities = sorted(counted_entities.iterkeys(), key=lambda k: counted_entities[k], reverse=True)


writer = csv.writer(open('../data/entity_distribution.csv', 'wb'))

for x in range(0,10):
    writer.writerow([sorted_entities[x], counted_entities[sorted_entities[x]]])