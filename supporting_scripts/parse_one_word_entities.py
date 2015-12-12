#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

with open("../data/entities.csv", "r") as text_file:
    text = text_file.readlines()

data = []

for line in text:
    entity = line.split(",")[1]
    if " " not in entity and entity != "entity_names":
        data.append(entity)
        #print entity

with open('../data/one_word_entities.txt', 'w') as outfile:
    json.dump(data, outfile)
