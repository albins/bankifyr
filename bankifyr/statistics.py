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


def histogram(data, sort=None):
    keys = list(data.keys())
    values = [-v for v in data.values()]
    if sort == "y":
        sorted_values, sorted_keys = zip(*sorted(zip(values, keys)))
    elif sort == "x":
        sorted_keys, sorted_values = zip(*sorted(zip(keys, values)))
    else:
        sorted_values, sorted_keys = values, keys

    plt.clf()
    plt.bar(range(len(sorted_keys)), sorted_values)
    plt.xticks(range(len(sorted_keys)), sorted_keys, rotation=50)


def split_months(rows):
    months = defaultdict(list)

    for row in rows:
        months[row[1].month].append(row)

    return months


def split_weekday(rows):
    weekdays = defaultdict(list)
    
    for row in rows:
        weekdays[row[1].isoweekday()].append(row)

    return weekdays

        
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


def filter_weekday(rows, day):
    result = []
    for row in rows:
        if row[1].isoweekday() == day:
            result.append(row)
    return result

def plot_everything(transactions):
    # Plot over each category over the entire timeline
    histogram(count_categories(transactions), sort="y")
    plt.savefig("categories.png")

    # Plot amount of money per weekday
    splitted_weedays = split_weekday(transactions)
    cost_per_day = dict.fromkeys(splitted_weedays.keys())
    
    for day in cost_per_day.keys():
        total = sum([x[2] for x in splitted_weedays[day]])
        cost_per_day[day] = total

    histogram(cost_per_day, sort="x")
    plt.savefig("weekdays.png")
    
    # Plot amount per category for every month
    splitted_months = split_months(transactions)
    for month in splitted_months.keys():
        histogram(count_categories(filter_month(splitted_months[month], month)), sort=True)
        plt.savefig(month_name(month) + ".png")

    # Plot the total amount of money for every month
    cost_per_month = dict.fromkeys(splitted_months.keys())
    for month in splitted_months.keys():
        total = sum([x[2] for x in splitted_months[month]])
        cost_per_month[month] = total

    histogram(cost_per_month, sort="x")
    plt.savefig("months.png")
