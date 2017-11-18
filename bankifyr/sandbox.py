import sys
import csv
import nltk
import random
import datetime
import numpy as np


def generate_features(e):
    name = e[0]
    date = e[1].split('-')
    amount = e[2]
    return {
            "first_word": name.split()[0].lower(),
            "last_word": name.split()[-1].lower(),
            "number_of_words": len(name.split()),
            "average_word_length": np.mean([len(word) for word in name.split()]),
            "day_of_the_week": datetime.date(*[int(n) for n in date]).weekday(),
            "day_of_the_month": int(date[2]),
            "month_of_the_year": int(date[1]),
            "year": int(date[0]),
            "amount": amount,
            }

with open(sys.argv[1], 'r') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=';')
    labeled_data = [
            (
                (row[0], row[1], float(row[2].replace(',', '.').replace(' ', ''))),
                row[3]
                )
            for i, row in enumerate(csv_reader) if row[3] and i
            ]

random.shuffle(labeled_data)

feature_sets = [(generate_features(e), label) for (e, label) in labeled_data]
train_set, test_set = feature_sets[::2], feature_sets[1::2]
classifier = nltk.NaiveBayesClassifier.train(train_set)

print(nltk.classify.accuracy(classifier, test_set))
classifier.show_most_informative_features(5)
