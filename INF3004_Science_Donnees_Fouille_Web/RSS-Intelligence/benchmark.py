import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as bs

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
    return Classifier().load_classif(lang).predict(items)

if __name__ == "__main__":
    lang = "fr"
    items = get_cleaned_items("./benchmark_gen.xml", lang)
    print(get_predict_class(items, lang))