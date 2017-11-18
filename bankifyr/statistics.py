#!/usr/bin/env python3

import sys
import csv
import nltk
import random
import datetime
import numpy as np
import daiquiri
import dateparser

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from collections import Counter
from collections import defaultdict

log = daiquiri.getLogger()

DEFAULT_DELIM = ";"
DEFAULT_SNIFF = 2048

def count_categories(rows):
    categories = Counter()
    for _, _, amount, category in rows:
        categories[category] += amount

    return categories


def read_rows(filename, labelled):
    with open(filename) as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(DEFAULT_SNIFF))
        csvfile.seek(0)
        log.info("Detected CSV dialect %s", dialect.__class__.__name__)
        csv_reader = csv.reader(csvfile, delimiter = "\t"
        )
        for row in csv_reader:
            if labelled and len(row) != 4:
                log.warning("Skipping invalid data row %s", str(row))
                continue

            date = dateparser.parse(row[1])
            amount = to_number(row[2])
            if labelled:
                yield ((row[0], date, amount), row[3])
            else:
                yield (row[0], date, amount)

def to_number(s):
    return float(s.replace(" ", "").replace(",", "."))


def histogram(data):
    keys = list(data.keys())
    values = [-v for v in data.values()]
    sorted_values, sorted_keys = zip(*sorted(zip(values, keys)))

    with PdfPages("foo.pdf") as pp:
        ones = [1 for _ in range(1, len(sorted_keys) + 1)]
        plt.bar(range(len(sorted_keys)), sorted_values)
        plt.xticks(range(len(sorted_keys)), sorted_keys, rotation=50)
        pp.savefig()


if __name__ == '__main__':
    filename = sys.argv[1]
    rows = read_rows(filename)
    cat_count = count_categories(rows)
    histogram(cat_count)
