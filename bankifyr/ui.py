def ask_for_category(transaction, confidence, categories):
    print("The following transaction only has confidence %d"
          .format(confidence))

    print("Choose a category %d--%d, or enter a new one: "
          .format(1, len(categories)))
