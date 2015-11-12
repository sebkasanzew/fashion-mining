# -*- coding: utf-8 -*-

import logging

from gensim import corpora, models, similarities

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
print "This is a test for gensim!"

# placeholder for json data
data = [{"url": "http://www.alealimay.com/blog/2014/10/10/aleali-may-web-launch-party", "sent_id": 0, "nouns": ["IA", "Thank", "everyone", "party"], "sentence": "IA\nThank you to everyone who made it out to my website launch party!"}, {"url": "http://www.alealimay.com/blog/2014/10/10/aleali-may-web-launch-party", "sent_id": 1, "nouns": ["start", "something", "outcome"], "sentence": "This is the start of something new and I was overly pleased with the outcome."}, {"url": "http://www.alealimay.com/blog/2014/10/10/aleali-may-web-launch-party", "sent_id": 2, "nouns": ["person", "website", "distance", "impact"], "sentence": "Each person who attended as well as supported my website from a distance has made such an impact."}, {"url": "http://www.alealimay.com/blog/2014/10/10/aleali-may-web-launch-party", "sent_id": 3, "nouns": ["everyone", "love", "support"], "sentence": "I appreciate everyone for the love and support."}, {"url": "http://www.alealimay.com/blog/2014/10/10/aleali-may-web-launch-party", "sent_id": 4, "nouns": ["Cheers"], "sentence": "Cheers!\n\u00a0\n"}, {"url": "http://www.alealimay.com/blog/2014/10/13/fools-gold-day-off", "sent_id": 5, "nouns": ["IA", "So", "friend", "ATrak", "Fools", "Gold", "Day", "Off", "Fest", "course"], "sentence": "IA\nSo my good friend ATrak invited me to his annual Fools Gold Day Off Fest... and of course I couldn't miss out."}, {"url": "http://www.alealimay.com/blog/2014/10/13/fools-gold-day-off", "sent_id": 6, "nouns": ["reunion", "creatives", "Vic", "Mensa", "Travis", "Scott", "Danny", "Brown", "Big", "Sean", "Chuck", "English", "Uzi", "Mike", "Carson", "Jerry", "Lorenzo", "others"], "sentence": "It turned out to be a reunion of great creatives such as Vic Mensa, Travis Scott, Danny Brown, Big Sean, Chuck English, Uzi, Mike Carson, Jerry Lorenzo and so many others."}, {"url": "http://www.alealimay.com/blog/2014/10/13/fools-gold-day-off", "sent_id": 7, "nouns": ["recap", "enjoy"], "sentence": "Here's a small recap, enjoy!\n"}, {"url": "http://www.alealimay.com/blog/2014/10/17/hypebeast-essentials", "sent_id": 8, "nouns": ["contact", "form", "right"], "sentence": "contact us\nUse the form on the right to contact us."}, {"url": "http://www.alealimay.com/blog/2014/10/17/hypebeast-essentials", "sent_id": 9, "nouns": ["text", "area", "change", "contact", "form", "submits", "edit", "mode", "modes", "right"], "sentence": "You can edit the text in this area, and change where the contact form on the right submits to, by entering edit mode using the modes on the bottom right."}, {"url": "http://www.alealimay.com/blog/2014/10/17/hypebeast-essentials", "sent_id": 10, "nouns": ["Email", "Address", "*"], "sentence": "Email Address *\n"}]
nouns_data = {"enjoy": [7], "everyone": [0, 3], "love": [3], "Thank": [0], "text": [9], "others": [6], "submits": [9], "Jerry": [6], "Carson": [6], "course": [5], "right": [8, 9], "Lorenzo": [6], "something": [1], "reunion": [6], "Fools": [5], "Email": [10], "Mensa": [6], "impact": [2], "Brown": [6], "Mike": [6], "Travis": [6], "recap": [7], "Big": [6], "support": [3], "*": [10], "Cheers": [4], "start": [1], "Fest": [5], "Address": [10], "party": [0], "Day": [5], "friend": [5], "mode": [9], "website": [2], "Danny": [6], "Off": [5], "form": [8, 9], "Vic": [6], "Chuck": [6], "creatives": [6], "So": [5], "English": [6], "IA": [0, 5], "change": [9], "modes": [9], "distance": [2], "ATrak": [5], "Uzi": [6], "Gold": [5], "edit": [9], "area": [9], "person": [2], "contact": [8, 9], "Scott": [6], "Sean": [6], "outcome": [1]}


nouns_list = []

for d in data:
    nouns_list.append(d["nouns"])

dictionary = corpora.Dictionary(nouns_list)

print "#### Words with ID"
print dictionary.token2id

corpora.MmCorpus.serialize('/tmp/corpus.mm', [dictionary.doc2bow(text) for text in nouns_list])
corpus = corpora.MmCorpus('/tmp/corpus.mm')

doc = "Thank you to everyone who made it out to my website launch party"
vec_bow = dictionary.doc2bow(doc.split())

print
print "##### TEST:"
print doc
print vec_bow
