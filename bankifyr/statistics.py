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


def read_rows(filename):
    with open(filename) as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(DEFAULT_SNIFF))
        csvfile.seek(0)
        csv_reader = csv.reader(csvfile, delimiter = "\t")
        for row in csv_reader:
            date = dateparser.parse(row[1])
            amount = to_number(row[2])
            yield (row[0], date, amount, row[3])

            
def to_number(s):
    return float(s.replace(" ", "").replace(",", "."))


def histogram(data, title):
    keys = list(data.keys())
    values = [-v for v in data.values()]
    sorted_values, sorted_keys = zip(*sorted(zip(values, keys)))

    plt.clf()
    plt.bar(range(len(sorted_keys)), sorted_values)
    plt.xticks(range(len(sorted_keys)), sorted_keys, rotation=50)


def split_months(rows):
    months = set()
    
    for row in rows:
        months.add(row[1].month)

    for month in months:
        histogram(count_categories(filter_month(rows, month)),
                  month_name(month))
        plt.savefig(month_name(month) + ".png")
        
        
def month_name(n):
    if n is 1:
       return "January"
    elif n is 2:
       return "February"
    elif n is 3:
       return "March"
    elif n is 4:
       return "April"
    elif n is 5:
       return "May"
    elif n is 6:
       return "June"
    elif n is 7:
       return "July"
    elif n is 8:
       return "August"
    elif n is 9:
       return "September"
    elif n is 10:
       return "October"
    elif n is 11:
       return "November"
    elif n is 12:
       return "December"

        
def filter_month(rows, month):
    result = []
    for row in rows:
        if row[1].month == month:
            result.append(row)
    return result
            

if __name__ == '__main__':
    filename = sys.argv[1]
    rows = read_rows(filename)
    split_months(list(rows))
