#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from bson.objectid import ObjectId

with open("../data/input_data/crawler.json", "r") as documents_file:
    docs = json.load(documents_file)

result = []

for doc in docs:
    tmp = {"url": doc["url"], "_id": {"$oid": str(ObjectId())}, "extracted_text": doc["extracted_text"]}
    print tmp
    result.append(tmp)


with open("../data/input_data/crawler_with_ids.json", "w") as docs_tags:
    json.dump(result, docs_tags, sort_keys=True, indent=4, ensure_ascii=True)

