#!/usr/bin/env python
# -*- coding: utf-8 -*-

import decimal
import json
from pprint import pprint
import lxml
from lxml.html import builder as E


def uni2utf(string=str()):
    return unicode(string).encode('utf8')


def sort_2d_array(array=None):
    if array is None:
        array = []
    return sorted(array, key=lambda l: l[0], reverse=False)


def sort_3d_array(array=None):
    """TODO"""
    if array is None:
        array = []
    return sorted(array, key=lambda l: l[0], reverse=False)


def merge_intersected_indicies(array_one=None, array_two=None):
    if array_one is None:
        array_one = []

    if array_two is None:
        array_two = []

    if array_one[1] >= array_two[0]:
        return [array_one[0], array_two[1]]
    else:
        return False


def compare_docs(document1=None, document2=None):
    total = 0
    false_positive = 0
    true_positive = 0

    if document1 is None:
        document1 = [{"entities": ["a", "b"], "_id": "b1", "indicies": [[[1, 2], [4, 6]], [[8, 10]]]}]

    if document2 is None:
        document2 = [{"entities": ["a", "b", "c", "d"], "_id": "b1", "cosDist": [.7, .9, .2, .4], "indicies": [[[14, 18]], [[1, 2], [4, 6]], [[8, 10]], [[11, 13], [14, 16]]]}]

    for doc2 in document2:
        print doc2
        for i, val in enumerate(doc2):
            # print doc2["cosDist"], i
            cos = doc2["cosDist"][i]
            for j in doc2["indicies"][i]:
                j.append(cos)

    for doc1 in document1:
        for doc2 in document2:
            if doc1["_id"] == doc2["_id"]:
                compared = compare_indices(doc1["indicies"], doc2["indicies"])
                print "compared", compared

    # calc_precision_recall()

    return


def compare_indices(indices1, indices2):
    indices1 = extract_indices(indices1)
    indices2 = extract_indices(indices2)

    indices1 = sorted(indices1)
    indices2 = sorted(indices2)

    print "1:", indices1
    print "2:", indices2

    doc_compare = []

    for i in indices1:
        for j in indices2:
            if indices2:
                false_negative = 0
                false_positive = 0
                true_positive = 0
                # result = {"cos": j[""], "count": [false_negative, false_positive, true_positive]}
            # doc_compare.append(result)

    return doc_compare


def calc_precision_recall(cos, data):
    filtered = []

    # for i, val in enumerate(data):
        # if data["cos"] >


def extract_indices(array=None):
    if array is None:
        array = []

    new_list = []

    for i in array:
        for j in i:
            new_list.append(j)

    return new_list


def insert_in_string(string=str(), index=int(), insert=str()):
    return string[:index] + insert + string[index:]
    # return string


def replace_gt_and_lt(string=str()):
    return string.replace('&gt;', '>').replace('&lt;', '<')


def format_number(num):
    try:
        dec = decimal.Decimal(num)
    except:
        return Exception.message
    tup = dec.as_tuple()
    delta = len(tup.digits) + tup.exponent
    digits = ''.join(str(d) for d in tup.digits)
    if delta <= 0:
        zeros = abs(tup.exponent) - len(tup.digits)
        val = '0.' + ('0' * zeros) + digits
    else:
        val = digits[:delta] + ('0' * tup.exponent) + '.' + digits[delta:]
    val = val.rstrip('0')
    if val[-1] == '.':
        val = val[:-1]
    if tup.sign:
        return '-' + val
    return val


def open_json(path=str()):
    print "opened file in path: ", path
    with open(path, mode="r") as data:
        return json.load(data, encoding="utf-8")


def export_html(path=str()):
    lxml.html.open_in_browser(path)


def create_html(data=None, tags=None):
    if tags is None:
        tags = {}
    if data is None:
        data = {}

    brand_tag_start = '<span class="brand" style="color: red">'
    brand_tag_end = '</span>'

    sections = []

    for docs in data:
        doc_id = uni2utf(docs["_id"]["$oid"])
        text = docs["extracted_text"]

        for tag in tags:
            if tag["_id"] == doc_id:
                indicies = sort_2d_array(extract_indices(tag["indicies"]))

                # remove all intersecting indicies
                restart = True
                while restart:
                    for i, val in enumerate(indicies):
                        if i < len(indicies) - 1:
                            value = merge_intersected_indicies(indicies[i], indicies[i + 1])
                            if value:
                                indicies[i] = value
                                del indicies[i + 1]
                                break
                        else:
                            restart = False

                added = 0
                for index in indicies:
                    j = index[0] + added
                    text = insert_in_string(text, j, brand_tag_start)
                    added += len(brand_tag_start)
                    j = index[1] + added
                    text = insert_in_string(text, j, brand_tag_end)
                    added += len(brand_tag_end)
                    print added

        sections.append(E.E.section(text, id=doc_id, style="margin: 10px"))

    head = E.HEAD()
    body = E.BODY(*sections)

    # print sections

    html = E.HTML(head, body)

    # pretty string
    # print "<!Doctype html>\n" + lxml.html.tostring(html, pretty_print=True)
    return replace_gt_and_lt("<!Doctype html>\n" + lxml.html.tostring(html, pretty_print=True))
