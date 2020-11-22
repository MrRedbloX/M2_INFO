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

    def tokenize(self, str_, lang):
        sw = get_stop_words(lang)
        words = [word_tokenize(sent) for sent in sent_tokenize(self.cleaner.clean_syntax(str_).lower().strip())]

        for i in range(len(words)):
            words[i] = [w for w in words[i] if w not in sw and not w.isdigit()]
        
        return words

    def enrich(self, collect=True, init=True):
        words = []

        if collect:
            Collector().feed_parser(path_main_input, path_main_output)

        f = shopen(path_main_output)
        for key in f.keys():
            if f[key]['language'] in langs:
                words.extend(self.tokenize(f[key]['title']+f[key]['description'] if f[key]['description'] is not None else "", f[key]['language']))

        word2vec = self.load()
        if init or word2vec is None:
            word2vec = Word2Vec(words, min_count=2)
        else:
            word2vec.train(words, total_examples=word2vec.corpus_count, epochs=word2vec.epochs)

        Word2Vec.save(word2vec, self.path)

    def load(self):
        if os.path.isfile(self.path):
            return Word2Vec.load(self.path)

    def get_word_vect(self):
        vect = self.load()
        if vect is not None:
            return vect.wv

    def most_similar(self, words):
        ret = []
        vect = self.get_word_vect()
        if vect is not None:
            for word in words:
                if word in vect.vocab:
                    ret.append(vect.most_similar(word))
        return ret

if __name__ == "__main__":
    enr = Enrichment()
    enr.enrich(collect=True, init=False)
    print(enr.most_similar(['virtuel']))