__author__ = 'cobauer'

from dictcc import Dict, AVAILABLE_LANGUAGES
import urllib2
from pyquery import PyQuery as pq
import pandas as pd
import re
from nltk.stem.snowball import SnowballStemmer
import distance
import urllib
from pattern.web import URL, extension

def _get_response(word, from_language, to_language):
        subdomain = from_language.lower()+to_language.lower()

        # req = urllib2.Request(
        #     "http://"+subdomain+".dict.cc/?s="+word,
        #     None,
        #     {'User-agent': 'Firefox/40.0.3'}
        # )
        url = URL("http://"+subdomain+".dict.cc/?s="+word)
        text = url.download()
        return text
        # return urllib2.urlopen(req).read()

def _sanity_check(df):
    n = df.shape[0]
    if n > 0:
        if df['term_0'].count() < n or df['term_1'].count() < n:
            print df
            print 'terms contain NaN!'
        #if min(df['term_0'].str.len()) < 2 or min(df['term_1'].str.len()) < 2:
        #    print 'terms with less than 2 letters!'

def get_dictcc_translation(term_words, language_in='en', language_out='de'):

    data = urllib2.quote(term_words)
    response = _get_response(data, language_in, language_out)

    q = pq(response)
    rows = q('tr[id^=\'tr\']')
    results = []
    stemmer = SnowballStemmer("english")

    for row in rows:
        result = {}
        #print q(row).outer_html()
        #q(q(rows[0])('td')[0]).outer_html()
        #q(rows[0]).remove('dfn').outer_html()
        result.update({'category_'+str(ix): q(t).text() for ix, t in enumerate(q(row)('dfn'))})
        q(row).remove('dfn')
        if 'category_0' not in result.keys():
            result['category_0'] = ''
        #result.update({'type_'+str(ix): q(t).text() for ix, t in enumerate(q(row)('var'))})
        #q(row).remove('var')
        q(row).remove('div')
        tds = q(row)('td')
        ix = 0
        for td in tds:
            text = q(td).text()
            if len(text) > 0:
                result.update({'type_'+str(ix): q(td)('var').text()})
                q(td).remove('var')
                text = q(td).text()
                m = re.search('([^\[]*)(.*)', text)
                term = m.group(1).strip()
                result_word = re.sub('-', ' ', term)
                result_word = re.sub('\'\w*', '', result_word)
                result_word = re.sub(' {2,}', ' ', result_word)
                #term = re.sub(' {2,}', ' ', term)
                term = term.split(' ')
                w2 = [stemmer.stem(w) for w in term]
                term = ' '.join(w2)

                result['term_'+str(ix)] = m.group(1).strip()
                result['term_stripped_'+str(ix)] = result_word
                result['term_stemmed_'+str(ix)] = term
                result['attributes_'+str(ix)] = m.group(m.lastindex).strip()
                ix += 1
        if result['type_1'] == '{pl}' and len(result['type_0']) == 0:
            result['type_0'] = '{pl}'
        if result['type_0'] == '{pl}' and len(result['type_1']) == 0:
            result['type_1'] = '{pl}'
        if result['type_1'] in ['{m}', '{f}', '{n}'] and len(result['type_0']) == 0:
            result['type_0'] = '{sg}'
        if result['type_0'] == '{adj}' and len(result['type_1']) == 0:
            result['type_1'] = '{adj}'
        results.append(result)
    df = pd.DataFrame(data=results)
    _sanity_check(df)
    if df.shape[0] > 0:
        word = re.sub('-', ' ', term_words)
        word = re.sub('\'\w*', '', word)
        word = re.sub(' {2,}', ' ', word)
        words = word.split(' ')
        w2 = [stemmer.stem(w) for w in words]
        term_stemmed = ' '.join(w2)
        #df.loc[:, 'term_0'] = df['term_0'].str.replace('-', ' ')
        #df.loc[:, 'term_0'] = df['term_0'].str.replace(' {2,}', ' ')
        df.loc[:, 'term_stemmed_0'] = df['term_stemmed_0'].str.replace('-', ' ')
        df.loc[:, 'term_stemmed_0'] = df['term_stemmed_0'].str.replace(' {2,}', ' ')

        #df.loc[:, 'term_1'] = df['term_1'].str.replace('-', ' ')
        #df.loc[:, 'term_1'] = df['term_1'].str.replace(' {2,}', ' ')
        df.loc[:, 'similarity'] = df['term_stemmed_0'].apply(lambda ww: 1 - distance.nlevenshtein(term_stemmed.lower(), ww.lower(), method=2))
        df.loc[:, 'similarity_notstemmed'] = df['term_stripped_0'].apply(lambda ww: 1 - distance.nlevenshtein(word.lower(), ww.lower(), method=2))
        df.loc[:, 'original_word'] = term_words
        df.loc[:, 'original_word_stemmed'] = term_stemmed
        df.loc[:, 'original_word_stripped'] = word
        df.sort(columns=['similarity', 'similarity_notstemmed'], ascending=[0, 0], inplace=True)
    return df





if __name__ == '__main__':
    df = get_dictcc_translation('Ankle Strap sandals')
    print df.head(1)