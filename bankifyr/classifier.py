import nltk
import numpy as np

import daiquiri

log = daiquiri.getLogger()

def generate_features(entry):
    name = entry[0]
    date = entry[1]
    amount = entry[2]
    return {
            "first_word": name.split()[0].lower(),
            "last_word": name.split()[-1].lower(),
            "number_of_words": len(name.split()),
            "average_word_length": np.mean([len(word) for word in name.split()]),
            "day_of_the_week": date.weekday(),
            "day_of_the_month": date.day,
            "month_of_the_year": date.month,
            "year": date.year,
            "amount": amount,
            }

class Classifier:
    def __init__(self, initial_data):
        self.train_data = initial_data
        self.classifier = nltk.NaiveBayesClassifier.train(
                [(generate_features(entry), label) for entry, label in self.train_data])

    def add_train_data(self, new_data):
        self.train_data += new_data
        self.classifier = nltk.NaiveBayesClassifier.train(
                [(generate_features(entry), label) for entry, label in self.train_data])

    def classify(self, data, threshold):
        classified_data = []
        for entry in data:
            guess = self.classifier.classify(generate_features(entry))
            pdist = self.classifier.prob_classify(generate_features(entry))
            confidence = np.var([pdist.prob(sample) for sample in pdist.samples()])
            log.debug("Classified an entry with confidence %f", confidence)
            if  confidence < threshold:
                label = self.ask_for_category(entry, list(pdist.samples()), confidence)
                self.add_train_data(self, [(entry, label)]
                classified_data.append((
                    entry,
                    label,
                    ))
            else:
                classified_data.append((entry, guess))
        return classified_data

    def ask_for_category(self, transaction, categories, confidence):
        print("The following transaction has a confidence rating of {}:"
              .format(confidence))
        print(transaction)
        print("Choose a category {}--{}, or enter a new one: ".format(1, len(categories)))
        print(*["{}. {}".format(i, category)
            for i, category in enumerate(categories)], sep='\n')
        answer = input()
        try:
            label = categories[int(answer)]
        except ValueError:
            label = answer
        return label

if __name__ == "__main__":
    import sys
    import csv
    import random
    import datetime

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

        train_entries, test_entries = labeled_data[::2], labeled_data[1::2]
        classifier = Classifier(train_entries)

        classifier.classify([entry for entry, label in test_entries])
