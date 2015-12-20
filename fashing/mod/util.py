import decimal
import json
from pprint import pprint


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
        val = '0.' + ('0'*zeros) + digits
    else:
        val = digits[:delta] + ('0'*tup.exponent) + '.' + digits[delta:]
    val = val.rstrip('0')
    if val[-1] == '.':
        val = val[:-1]
    if tup.sign:
        return '-' + val
    return val


def open_json(path):
    with open(path, mode="r") as data:
        return json.load(data.readlines())


def export_html(data):
    for docs in data:
        pprint(docs)

    return 0
