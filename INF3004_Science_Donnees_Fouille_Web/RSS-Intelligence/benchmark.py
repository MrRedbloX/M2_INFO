import sys

import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as bs
from json import dumps

from classifier import Cleaner, Classifier, DictClassifer

def get_items(filename):
    return ET.parse(filename).getroot().find("channel").findall("item")

def items_to_list(items):
    for item in items:
        yield item.find("title").text + item.find("description").text + item.find("text").text

def clean_items(items, lang):
    cleaner = Cleaner()
    for item in items:
        yield cleaner.clean_str(''.join(bs(item, features='lxml').findAll(text=True)), lang)

def get_cleaned_items(filename, lang):
    return list(clean_items(items_to_list(get_items(filename)), lang))

def get_predict_class(items, lang):
    return Classifier().load_classif(lang).predict(items, return_predict_classes=True)

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

def to_json(filename, dict_):
    with open(filename, 'w') as f:
        f.write(dumps(dict_))


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        lang = sys.argv[2]
        names = ['COGOLUEGNES']
        print("Starting to classify...")
        result = to_dict(get_predict_class(get_cleaned_items(filename, lang), lang), lang, names)
        to_json(names[0]+"_"+result['method']+"_"+lang+".res", result)
        print("Done.")
    except Exception as e:
        print(e)
        print("usage: benchmark <filename> <lang>")