import json
import nltk

with open("../data/entities.txt", "r") as text_file:
    dict = text_file.readlines()

with open("../data/plain_text_optimized_eng.json", "r") as text_file:
    docs = text_file.readlines()

dict = eval(dict[0])

data = []
entity_counter = {}

i = 0
l = len(docs)

with open("../data/test.json", "a") as myfile:
    myfile.seek(0)
    myfile.truncate()

    for line in docs:
        json_data = json.loads(line)
        contains = False


        for entity in dict:
            #if entity.lower() in json_data["extracted_text"].lower():
            if entity in json_data["extracted_text"]:
                contains = True
                if entity in entity_counter.keys():
                    entity_counter[entity] = entity_counter[entity] + 1
                else:
                    entity_counter[entity] = 1

        if contains:
            myfile.write(line + ",")

        i+=1
        print str(i) + "/" + str(l)

print entity_counter