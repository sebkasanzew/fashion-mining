# -*- coding: utf-8 -*-

import json
import nltk

print("This is a Test for NLTK!")

### read data file and put every json into an array
with open("data/plain_text.json", "r") as text_file:
    text = text_file.readlines()
#print(text[0])

data = []
nouns_data = {}
sent_id = 0

for x in range(0,3):
    ### reads first json
    json_data = json.loads(text[x])

    #print(json_data)
    extracted_text = json_data["extracted_text"]

    #Sentence Tokenization
    sentences = nltk.sent_tokenize(extracted_text)
    #print(sentences)
    for s in sentences:
        #Word tokenization and tagging
        words_with_tags = nltk.tag.pos_tag(nltk.word_tokenize(s))
        nouns = []
        for w in words_with_tags:
            if w[1] == "NN" or w[1] =="NNP" or w[1] =="NNPS" or w[1] =="NNS":
                nouns.append(w[0])

                #list with only nouns and ids
                if (w[0] not in nouns_data):
                    nouns_data[w[0]] = [sent_id]
                else:
                    # add the sent_id to the existing noun
                    nouns_data[w[0]].append(sent_id)

        data.append({"url":json_data["url"], "sent_id":sent_id, "sentence": s, "nouns": nouns})
        sent_id += 1

print json.dumps(data)
print nouns_data


