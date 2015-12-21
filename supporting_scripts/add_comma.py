#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

with open("../data/plain_text_optimized_eng_filtered.json", "r") as text_file:
    docs = text_file.readlines()

with open("../data/test.json", "a") as myfile:
    myfile.seek(0)
    myfile.truncate()

    for doc in docs:
        doc = str(json.dumps(json.loads(doc))) + ",\n"
        myfile.write(doc)