from sys import argv
from multiprocessing import cpu_count, Pool

import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as bs
from json import dumps
from numpy import append as nappend

from classifier import Cleaner, Classifier, DictClassifer

"""
Returns the items in the xml file that follows a specific given structure.
"""
def get_items(filename):
    return ET.parse(filename).getroot().find("channel").findall("item")

"""
Yields for each item a string representation.
"""
def items_to_list(items):
    for item in items:
        yield item.find("title").text + item.find("description").text + item.find("text").text

"""
Returns a cleaned items
"""
def clean_item(item, cleaner, lang):
    return cleaner.clean_str(''.join(bs(item, features='lxml').findAll(text=True)), lang)

"""
From a list of items, returns a cleaned version
"""
def clean_items(items, cleaner, lang):
    return parallelize(items, clean_item, [cleaner, lang])

"""
Returns the predict class of an item
"""
def predict_class(item, clf):
    return clf.predict(item, return_predict_classes=True)

"""
From a list of cleaned items, returns the correspondind predict classes with also the value of the decision function for each class.
"""
def predict_classes(items, clf):
    return parallelize(items, predict_class, [clf])

"""
Executes operations on element in list in parallel
"""
def parallelize(lst, func, args):
    pool = Pool(cpu_count())
    results = [pool.apply_async(func, args=tuple(nappend([elt], args))) for elt in lst]
    pool.close()
    pool.join()
    return list(map(lambda p: p.get(), results))

"""
Builds a dict given a specific expectation for the structure.
"""
def to_dict(classes, lang, names):
    res = {}
    predicted = []
    probs = []

    for class_ in classes:
        predicted.append(class_[0])
        probs.append(list(class_[1].values()))
    
    res['pred'] = predicted
    res['probs'] = probs
    res['names'] = names
    res['method'] = 'DictClassifier(custom)'
    res['lang'] = lang

    return res

"""
Writes the dict to a json file.
"""
def to_json(filename, dict_):
    with open(filename, 'w') as f:
        f.write(dumps(dict_))

"""
Creates a JSON file from a specific xml file and a language.
filename: xml file.
lang: language of the feeds in the xml file.
"""
if __name__ == "__main__":
    try:
        filename = argv[1]
        lang = argv[2]
        names = ['COGOLUEGNES'] # Can be modified
        clf = Classifier().load_classif(lang)
        cleaner = Cleaner()

        print("Parsing items...")
        items = list(items_to_list(get_items(filename)))
        print(f"{len(items)} items parsed.")
        print("Cleaning...")
        cleaned_items = clean_items(items, cleaner, lang)
        print("Classifying...")
        predicted_classes = predict_classes(cleaned_items, clf)
        print("Saving to json...")
        result = to_dict(predicted_classes, lang, names)
        to_json(f"{names[0]}_{result['method']}_{lang}.res", result)
        print("Done.")

    except Exception as e:
        print(e)
        print("usage: benchmark <filename> <lang>")