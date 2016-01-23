#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re

from bson.objectid import ObjectId

with open("../data/input_data/crawler.json", "r") as documents_file:
    docs = json.load(documents_file)

result = []

for doc in docs:
    #text = str(doc["url"]).translate(None, '[]{}*')

    text = str(doc["extracted_text"].encode("utf8")).translate(None, '[]{}*')

    tmp = {"url": doc["url"], "_id": {"$oid": str(ObjectId())}, "extracted_text": text}
    result.append(tmp)


with open("../data/input_data/crawler_with_ids.json", "w") as docs_tags:
    json.dump(result, docs_tags, sort_keys=True, indent=4, ensure_ascii=True)

