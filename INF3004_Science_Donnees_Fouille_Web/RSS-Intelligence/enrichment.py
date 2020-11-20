# import nltk
# nltk.download('punkt')

import os

from gensim.models import Word2Vec
from nltk import sent_tokenize, word_tokenize

from stop_words import get_stop_words

from shelve import open as shopen
from pickle import load, loads, dump, dumps

from collector import Collector
from config import path_main_input, path_main_output, langs, path_res
from classifier import Cleaner

class Enrichment:

    def __init__(self):
        self.cleaner = Cleaner()
        self.path = path_res+"/enrich/vect"

    def load(self):
        if os.path.isfile(self.path):
            with open(self.path, 'rb') as f:
                return loads(load(f))

    def store(self, vects):
        with open(self.path, 'wb') as f:
            dump(dumps(vects), f)

    def tokenize(self, str_, lang):
        sw = get_stop_words(lang)
        return [word for word in [word_tokenize(sent) for sent in sent_tokenize(self.cleaner.clean_syntax(str_).lower())] if word not in sw]

    def enrich(self, collect=True):
        words = []

        if collect:
            Collector().feed_parser(path_main_input, path_main_output)

        f = shopen(path_main_output)
        for key in f.keys():
            if f[key]['language'] in langs:
                words.extend(self.tokenize(f[key]['title']+f[key]['description'] if f[key]['description'] is not None else "", f[key]['language']))

        word2vec = Word2Vec(words, min_count=2)
        self.store(word2vec.wv)

if __name__ == "__main__":
    enrichment = Enrichment()
    enrichment.enrich(collect=False)
    vects = enrichment.load()
    # print(vects.vocab)
    print(vects.most_similar('contacts'))

