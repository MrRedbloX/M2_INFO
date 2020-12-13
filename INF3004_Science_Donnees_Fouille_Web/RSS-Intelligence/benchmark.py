from sys import argv

import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as bs
from json import dumps

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
From a list of stringify items, yields the cleaned string.
"""
def clean_items(items, lang):
    cleaner = Cleaner()
    for item in items:
        yield cleaner.clean_str(''.join(bs(item, features='lxml').findAll(text=True)), lang)

"""
From a xml filename, returns a list of cleaned items.
"""
def get_cleaned_items(filename, lang):
    return list(clean_items(items_to_list(get_items(filename)), lang))

"""
From a list of cleaned items, returns the correspondind predict classes with also the value of the decision function for each class.
"""
def get_predict_class(items, lang):
    return Classifier().load_classif(lang).predict(items, return_predict_classes=True)

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
        print("Starting to classify...")
        result = to_dict(get_predict_class(get_cleaned_items(filename, lang), lang), lang, names)
        to_json(names[0]+"_"+result['method']+"_"+lang+".res", result)
        print("Done.")
    except Exception as e:
        print(e)
        print("usage: benchmark <filename> <lang>")