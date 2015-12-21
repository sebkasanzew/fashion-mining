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


def extract_indicies(array=None):
    if array is None:
        array = []

    new_list = []

    for i in array:
        for j in i:
            new_list.append(j)

    return new_list


def insert_in_string(string=str(), index=int(), insert=str()):
    return string[:index] + insert + string[index:]


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
                # print uni2utf(tag["entities"])
                indicies = sort_2d_array(extract_indicies(tag["indicies"]))
                # print(indicies)

                # print indicies

                added = 0
                for index in indicies:
                    j = index[0] + added
                    text = insert_in_string(text, int(j), brand_tag_start)
                    added += len(brand_tag_start)
                    j = index[1] + added
                    text = insert_in_string(text, int(j), brand_tag_end)
                    added += len(brand_tag_end)

        sections.append(E.E.section(text, id=doc_id, style="margin: 10px"))

    head = E.HEAD()
    body = E.BODY(*sections)

    # print sections

    html = E.HTML(head, body)

    # pretty string
    # print "<!Doctype html>\n" + lxml.html.tostring(html, pretty_print=True)
    return replace_gt_and_lt("<!Doctype html>\n" + lxml.html.tostring(html, pretty_print=True))
