#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

with open("../data/entities.csv", "r") as text_file:
    text = text_file.readlines()

data = []

for line in text:
    entity = line.split(",")[1]
    if entity != "entity_names":
        data.append(str(entity))

print str(data)

with open('../data/entities.txt', 'w') as outfile:
    json.dump(data, outfile)
