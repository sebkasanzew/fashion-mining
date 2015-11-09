#!/usr/bin/python
# coding: utf-8

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

###Here insert connection to NLTK - JSON INPUT

print("#################### From Strings to Vectors ########################")

from gensim import corpora, models, similarities

documents = ["Kanye West brings new Nike sneaker collection",
             "One shoe to conquer the world in New York",
             "A star was seen with new sneaker model",
             "This Summer blue jeans are totally hot",
             "Karl Lagerfeld announced new fashion collection this summer",
             "The evening dress from Eva Padberg was amazing",
             "Is it fashion to wear jogging pants",
             "This jeans from Katy Perry was old-fashioned",
             "Every people want the new Nike Sneaker from Kanye"]

stoplist = set('for a of the and to in is are'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in documents]

from collections import defaultdict

frequency = defaultdict(int)
for text in texts:
  for token in text:
    frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1]
         for text in texts]

from pprint import pprint

pprint(texts)

dictionary = corpora.Dictionary(texts)
dictionary.save('/tmp/deerwester.dict')  # store the dictionary, for future reference
print(dictionary)

print(dictionary.token2id)

new_doc = "Nike sneaker collection"
new_vec = dictionary.doc2bow(new_doc.lower().split())
print(new_vec)  # the word "interaction" does not appear in the dictionary and is ignored

corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('/tmp/deerwester.mm', corpus)  # store to disk, for later use
print(corpus)

print("############################## END ########################")
print("\n")
print("################### Corpus Streaming – One Document at a Time #################")
print("\n")
print("################### Sequential Document Vector load ####################")


class MyCorpus(object):
  def __iter__(self):
    for line in open('mycorpus.txt'):
      # assume there's one document per line, tokens separated by whitespace
      yield dictionary.doc2bow(line.lower().split())


corpus_memory_friendly = MyCorpus()  # doesn't load the corpus into memory!
print(corpus_memory_friendly)

for vector in corpus_memory_friendly:  # load one vector into memory at a time
  print(vector)

print("\n")
print("################### Construct Dict sequential ####################")
# collect statistics about all tokens
dictionary = corpora.Dictionary(line.lower().split() for line in open('mycorpus.txt'))
# remove stop words and words that appear only once
stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
dictionary.filter_tokens(stop_ids + once_ids)  # remove stop words and words that appear only once
dictionary.compactify()  # remove gaps in id sequence after words that were removed
print(dictionary)
