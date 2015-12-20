#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

with open("../data/example_docs.json", "r") as text_file:
    docs = text_file.readlines()

for doc in docs:
    print doc
    json_data = json.loads(doc)
    #print "X"
    #print json_data