# Following commented code might has to be executed once.
# import nltk
# nltk.download('punkt')

from os import path

from gensim.models import Word2Vec
from nltk import sent_tokenize, word_tokenize

from stop_words import get_stop_words

from shelve import open as shopen

from collector import Collector
from classifier import Cleaner
from config import path_main_input, path_main_output, langs, path_res

class Enrichment:

    """
    Init of Enrichment class.
    Assign a cleaner.
    Creates a path for the vect.
    """
    def __init__(self):
        self.cleaner = Cleaner()
        self.path = path_res+"/enrich/vect"

    """
    Returns a list which contains list of cleaned words (sentence).
    """
    def tokenize(self, str_, lang):
        sw = get_stop_words(lang)
        words = [word_tokenize(sent) for sent in sent_tokenize(self.cleaner.clean_syntax(str_).lower().strip())]

        for i in range(len(words)):
            words[i] = [w for w in words[i] if w not in sw and not w.isdigit()]
        
        return words

    """
    Trains the word2vec vector.
    If collect is True, runs the feed parser.
    If init is True it will create a new vector.
    """
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

    """
    Loads the vector.
    """
    def load(self):
        if path.isfile(self.path):
            return Word2Vec.load(self.path)

    """
    Returns the word vector of word2vec.
    """
    def get_word_vect(self):
        vect = self.load()
        if vect is not None:
            return vect.wv

    """
    Returns a list of words that are similar to the given one according to the vector.
    The returned list can be empty.
    """
    def most_similar(self, words):
        ret = []
        vect = self.get_word_vect()
        if vect is not None:
            for word in words:
                if word in vect.vocab:
                    ret.append(vect.most_similar(word))
        return ret

"""
First enrich with new feeds and then prints the most similar words of a given word.
"""
if __name__ == "__main__":
    enr = Enrichment()
    enr.enrich(collect=True, init=False)
    print(enr.most_similar(['virtuel'])) # Change the word here.