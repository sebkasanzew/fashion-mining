#!/usr/bin/env python
# -*- coding: utf-8 -*-

import decimal
import json
from pprint import pprint
import lxml  # xml functions
from lxml.html import builder as E  # for building a html document


def uni2utf(string=str()):
    """
    Converts an unicode string into an utf-8 string.
    :param string: the unicode string
    :type string: str
    :return: An UTF-8 string
    :rtype: str
    """
    return unicode(string).encode('utf8')


def sort_2d_array(array=None):
    """
    Sort a 2D array after the first number ascending.
    :param array: unsorted 2D-list
    :type array: list
    :return: sorted 2D-list
    :rtype: list[list[int]]
    """
    if array is None:
        return []
    return sorted(array, key=lambda l: l[0], reverse=False)


def sort_3d_array(array=None):
    # TODO: seems to do the same like sort_2d_array()
    """
    Sort a 3D array after the first number ascending.
    :param array: unsorted 3D-list
    :type array: list
    :return: sorted 3D-list
    :rtype: list[list[list[int]]]
    """
    if array is None:
        return []
    return sorted(array, key=lambda l: l[0], reverse=False)


def merge_intersected_indices(array_one=None, array_two=None):
    """
    Merges two list elements into one list if they ave an intersection.
    :param array_one: first list element
    :param array_two: second list element
    :type array_one: list[int]
    :type array_two: list[int]
    :return: returns the intersected list.
    :rtype: list[int]
    """
    if array_one is None:
        array_one = []

    if array_two is None:
        array_two = []

    if array_one[1] >= array_two[0]:
        return [array_one[0], array_two[1]]
    elif (array_two[1] >= array_one[0]) and (array_two[0] < array_one[0]):  # if the given parameters are switched
        return [array_two[0], array_one[1]]
    else:
        return False


def compare_docs(gold_document=None, w2v_document=None, mode=None, steps=0.05):
    # STEP 1
    """
    Compares two documents/sentences.
    :param gold_document: the document with the gold standard
    :param w2v_document: the document generated by word2vec
    :param mode: the data calculation mode
    :param steps: the precision of the graph
    :type gold_document: list
    :type w2v_document: list
    :type mode: str
    :type steps: float
    :return: A 2D-list with the graph data. The values should be between 0 and 1.
    :rtype: list[list[int]]
    """
    if (gold_document is None) or (gold_document is False):
        gold_document = [{"entities": ["a", "b"],
                          "_id": "b1",
                          "indices": [
                              [[1, 2], [4, 6]],
                              [[8, 10]],
                              [[22, 32]]
                          ]}]

    if (w2v_document is None) or (w2v_document is False):
        w2v_document = [{"entities": ["a", "b", "c", "d"],
                         "_id": "b1",
                         "cos_dist": [["wort", .7], ["wort", .9], ["wort", .2], ["wort", .4]],
                         "indices": [
                             [[14, 18]],
                             [[1, 2], [4, 6]],
                             [[8, 10]],
                             [[11, 13], [14, 16]]
                         ]}]

    # add the cos_dist to the indices array
    for w2v_doc in w2v_document:
        for i, val in enumerate(w2v_doc["indices"]):
            cos = uni2utf(w2v_doc["cos_dist"][i][1])
            if cos == "None":  # TODO needs some more thinking
                cos = 0
            cos = float(cos)
            for j in w2v_doc["indices"][i]:
                j.append(cos)

    compared = []

    for gold_doc in gold_document:
        for w2v_doc in w2v_document:
            if gold_doc["_id"] == w2v_doc["_id"]:  # check if the sentences are identical
                append = compare_indices(gold_doc["indices"], w2v_doc["indices"])
                compared.append(append)
                # print "compared:"
                # print pprint(compared)

    graph_data = []

    if mode == "precision":
        for i in step_range(0, 1, steps):
            pr = calc_cos_precision(i, compared)
            graph_data.append(pr)
    elif mode == "recall":
        for i in step_range(0, 1, steps):
            pr = calc_cos_recall(i, compared)
            graph_data.append(pr)
    else:
        for i in step_range(0, 1, steps):
            pr = calc_precision_recall(i, compared)
            graph_data.append(pr)

    graph_data = sorted(graph_data)

    print "\n[recall, precision]"
    pprint(graph_data)

    return graph_data


def compare_indices(gold_indices, w2v_indices):
    # STEP 2
    # TODO: compare the indices in the correct way
    """
    :param gold_indices:
    :param w2v_indices:
    :return:
    """
    gold_indices = extract_indices(gold_indices)
    w2v_indices = extract_indices(w2v_indices)

    gold_indices = sorted(gold_indices)
    w2v_indices = sorted(w2v_indices)

    def check_tp_and_fp(gold_indices_list, w2v_index):
        for i, g_val in enumerate(gold_indices_list):
            if w2v_index[0] == gold_indices_list[i][0] and w2v_index[1] == gold_indices_list[i][1]:
                return {"cos": w2v_indices[key][2], "count": {"fn": 0, "fp": 0, "tp": 1}}

        return {"cos": w2v_index[2], "count": {"fn": 0, "fp": 1, "tp": 0}}

    def check_fn(w2v_indices_list, g_index):
        w2v_check = []

        # remove the "cos"-key for the check afterwards
        for i, val in enumerate(w2v_indices_list):
            w2v_check.append([val[0], val[1]])

        if g_index not in w2v_check:
            return {"cos": None, "count": {"fn": 1, "fp": 0, "tp": 0}}

        return False

    # print "compare_indices(): -----------------------------------"

    # print "gold:", gold_indices
    # print "w2v:", w2v_indices

    doc_compare = []

    for key, w2v_val in enumerate(w2v_indices):
        result = check_tp_and_fp(gold_indices, w2v_indices[key])
        doc_compare.append(result)

    for key, gold_val in enumerate(gold_indices):
        result = check_fn(w2v_indices, gold_indices[key])
        # print "result"
        # pprint(result)
        if result:
            doc_compare.append(result)

    return doc_compare


def calc_cos_precision(cos, data):
    all_tp_fp_fn = []

    for i in data:
        all_tp_fp_fn.append(count_all_tp_fp_fn(cos, i))

    tp = 0
    fp = 0
    fn = 0

    for i in all_tp_fp_fn:
        tp += i["tp"]
        fp += i["fp"]
        fn += i["fn"]

    print "\nValues for cosinus =", cos, ":"
    print "tp:", tp
    print "fp:", fp
    print "fn:", fn
    print "tn:", (tp + fn) - fp

    precision = calc_precision(tp, fp)

    return [cos, precision]


def calc_cos_recall(cos, data):
    all_tp_fp_fn = []

    for i in data:
        all_tp_fp_fn.append(count_all_tp_fp_fn(cos, i))

    tp = 0
    fp = 0
    fn = 0

    for i in all_tp_fp_fn:
        tp += i["tp"]
        fp += i["fp"]
        fn += i["fn"]

    print "\nValues for cosinus =", cos, ":"
    print "tp:", tp
    print "fp:", fp
    print "fn:", fn
    print "tn:", (tp + fn) - fp

    recall = calc_recall(tp, fn)

    return [cos, recall]


def calc_precision_recall(cos, data):
    all_tp_fp_fn = []

    for i in data:
        all_tp_fp_fn.append(count_all_tp_fp_fn(cos, i))

    tp = 0
    fp = 0
    fn = 0

    for i in all_tp_fp_fn:
        tp += i["tp"]
        fp += i["fp"]
        fn += i["fn"]

    print "\nValues for cosinus =", cos, ":"
    print "tp:", tp
    print "fp:", fp
    print "fn:", fn
    print "tn:", (tp + fn) - fp

    precision = calc_precision(tp, fp)
    recall = calc_recall(tp, fn)

    # [calc_precision(tp, fp), calc_recall(tp, fn)]

    # print "calc_precision_recall():", [recall, precision]

    return [recall, precision]


def count_all_tp_fp_fn(cos, data):
    filtered_data = []
    ignored_data = []

    # print "##################### P/R ######################"
    # print "data:"
    # pprint(data)

    for i in data:
        # print "cos:", cos
        # print "i:", i
        # print "i['cos']:", i["cos"]
        # print "data", data[0]

        if i["cos"] >= cos or i["cos"] is None:
            filtered_data.append(i)
        else:
            ignored_data.append(i)

    # print "filtered_data:"
    # pprint(filtered_data)
    #
    # print "ignored_data:"
    # pprint(ignored_data)

    tp = calc_tp(filtered_data)
    fp = calc_fp(filtered_data)
    fn = calc_fn(data, ignored_data)

    # pprint({"tp": tp, "fp": fp, "fn": fn})
    return {"tp": tp, "fp": fp, "fn": fn}


def calc_tp(doc):
    count = 0
    for i in doc:
        if i["count"]["tp"] == 1:
            count += 1
    return count


def calc_fp(doc):
    count = 0
    for i in doc:
        if i["count"]["fp"] == 1:
            count += 1
    return count


def calc_fn(doc, ignored_doc):
    count = 0

    for i in doc:
        if i["count"]["fn"] == 1:
            count += 1

    for i in ignored_doc:
        if i["count"]["tp"] == 1:
            count += 1

    return count


def calc_tn(doc):
    count = 0

    for i in doc:
        if i["count"]["tn"] == 1:
            count += 1

    return count


def extract_indices(array=None):
    """
    Extracts all indices from a specific nested list.
    :param array:
    :type array: list[list[int]]
    :return: A list of all extracted indices
    :rtype: list
    """
    if array is None:
        return []

    new_list = []

    for i in array:
        for j in i:
            new_list.append(j)

    return new_list


def insert_in_string(string=str(), index=int(), insert=str()):
    """
    Inserts a string in another string at the given index position.
    :param string: The base string where the other string will be inserted.
    :param index: The index at which position the string will be inserted.
    :param insert: The string to be inserted.
    :type string: str
    :type index: int
    :type insert: str
    :return: The base string with the inserted string at the given position.
    :rtype: str
    """
    return string[:index] + insert + string[index:]


def replace_gt_and_lt(string=str()):
    """
    Workaround the bug, where ">" and "<" signs are displayed in the final html document.
    :param string: buggy html document
    :type string: str
    :return: Cleaned up html document.
    :rtype: str
    """
    return string.replace('&gt;', '>').replace('&lt;', '<')


def format_number(num):
    """
    Turns a number into a rounded decimal, if its greater that 1. If it's lower that 1 than the float is reduced to one
    digit after the point.
    :param num: a floating number
    :type num: float
    :return: A rounded decimal number for better presentation on the GUI.
    :rtype: decimal
    """
    dec = None
    try:
        dec = decimal.Decimal(num)
    except Exception as e:
        print "format_number error: " + e.message
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
    """
    Opens a JSON-file from the given path.
    :param path: the path to the JSON-file
    :type path: str
    :return: the json as a list
    :rtype: list
    """
    print "opened file in path: ", path

    try:
        with open(path, mode="r") as data:
            return json.load(data, encoding="utf-8")
    except IOError as e:
        print "IOError:" + e.message
        return False


def export_html(path=str()):
    """
    Dunno, makes no sense to me. Just leave it like this for now
    :param path:
    :type path: str
    :return: Nothing
    :rtype: None
    """
    lxml.html.open_in_browser(path)


def create_html(data=None, tags=None):
    """
    Creates a HTML document out of specific json data.
    :param data: dict with
    [
        {
            "url": "<some url>",
            "_id": {
                "$oid": "<some id>"
            },
            "extracted_text": "<some text>"
        },
        ...
    ]
    :param tags: dict with
    [
        {
            "entities": ["<some entity>", ...],
            "_id": "<some id>",
            "indices": [<some index number>, ...]
        },
        ...
    ]
    :type data: list
    :type tags: list
    :return: Formatted html document as text.
    :rtype: str
    """
    if tags is None:
        tags = []
    if data is None:
        data = []

    brand_tag_start = '<span class="brand" style="color: red">'
    brand_tag_end = '</span>'

    sections = []

    for docs in data:
        doc_id = uni2utf(docs["_id"]["$oid"])
        text = docs["extracted_text"]

        for tag in tags:
            if tag["_id"] == doc_id:
                indices = sort_2d_array(extract_indices(tag["indices"]))

                # remove all intersecting indices
                restart = True
                while restart:
                    for i, val in enumerate(indices):
                        if i < len(indices) - 1:
                            value = merge_intersected_indices(indices[i], indices[i + 1])
                            if value:
                                indices[i] = value
                                del indices[i + 1]
                                break
                        else:
                            restart = False

                added = 0
                for index in indices:
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


def calc_precision(tp, fp):
    """
    Calculates the precision of a word2vec implementation.
    :param tp: true positives
    :param fp: false positives
    :type tp: int
    :type fp: int
    :return: The precision value for the given parameters.
    :rtype: float
    """
    precision = 0
    if (tp == 0) and (fp == 0):
        return precision
    else:
        precision = float(tp) / (tp + fp)
    return precision


def calc_recall(tp, fn):
    """
    Calculates the recall of a word2vec implementation.
    :param tp: true positives
    :param fn: false negatives
    :type tp: int
    :type fn: int
    :return: The recall value for the given parameters.
    :rtype: float
    """
    recall = float(tp) / (tp + fn)
    return recall


def step_range(start, stop, step):
    """
    A range function where you can set a step by which the iterator is raised.
    :param start: the start value
    :param stop: the stop value
    :param step: the number by which the iteration is increased
    :type start: int
    :type stop: int
    :type step: float
    :return: range value for loops
    :rtype: list[int]
    """
    r = start
    while round(r, 2) <= stop:
        yield round(r, 2)
        r += step
