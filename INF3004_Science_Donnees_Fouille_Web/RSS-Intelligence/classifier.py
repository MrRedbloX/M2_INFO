import os
from time import sleep

from shelve import open as shopen
from pickle import load, loads, dump, dumps
import numpy as np

from string import punctuation
from snowballstemmer import stemmer
from stop_words import get_stop_words
from sklearn.model_selection import train_test_split as tts

from collector import Collector
from config import langs, classes, path_res, path_main_input

collect = Collector()

class Utils:

    """
    Returns the path of input from a class name and a language.
    """
    def path_input(name, lang):
        return f'{path_res}/data/{name}/{lang}/input/urls.txt'

    """
    Returns the path of output from a class name and a language.
    """
    def path_output(name, lang):
        return f'{path_res}/data/{name}/{lang}/output/{name}_{lang}'

    """
    Returns the full language name from a acronym.
    Raises an exception if the language is not handled.
    """
    def lang_literal(lang):
        if lang == 'en':
            return 'english'
        elif lang == 'fr':
            return 'french'
        else:
            raise Exception(f'Unsuported lang {lang}.')
    
    """
    Returns the path to the vector from a language.
    """
    def path_vect(lang):
        return f'{path_res}/vect/{lang}/vect_{lang}'

    """
    Returns the path to the classifier from a language.
    """
    def path_classifier(lang):
        return f'{path_res}/classifier/{lang}/classifier_{lang}'

class Dataset:

    """
    Builds a dataset for every language and every class.
    Calls the feed_parser function from Collector.
    """
    def create_dataset():
        for lang in langs:
            for class_ in classes:
                print(f"{class_} - {lang.upper()}")
                collect.feed_parser(Utils.path_input(class_, lang), Utils.path_output(class_, lang))

class Cleaner:
    
    #Utiliser TextBlob pour corriger les fautes


    """
    Init of Cleaner
    Add some new punctuations to string punctuation
    """
    def __init__(self):
        self.puncts = punctuation
        self.puncts += '’«»'

    """
    Removes all punctuations from a string.
    """
    def clean_syntax(self, str_):
        ret = str_
        for punc in self.puncts:
            ret = str_.replace(str(punc), ' ')

        return ret.replace('\t', ' ').replace('\n', ' ').strip()


    """
    Removes stop words and digits from a string.
    Stems all remainded words.
    """
    def clean_grammar(self, str_, lang):
        cleaned = []
        sw = get_stop_words(lang)
        stem = stemmer(Utils.lang_literal(lang))
        for word in str_.split():
            if word not in sw and not word.isdigit():
                cleaned.append(stem.stemWord(word.lower()))
        return ' '.join(cleaned)
    
    """
    Clean the syntax then clear the grammar of a string.
    """
    def clean_str(self, str_, lang):
        return self.clean_grammar(self.clean_syntax(str_), lang)


    """
    Clean the title and the description (if exists) of a feed.
    Returns a concatenation of the cleaned title and description.
    """
    def clean_feed(self, feed, limit=False, limit_size=50):
        clean_txt = self.clean_str(feed['title'], feed['language'])
        if feed['description'] is not None:
            desc = feed['description']
            if limit:
                desc = desc[:limit_size]
            clean_txt += " "+self.clean_str(desc, feed['language'])
        return clean_txt


    """
    For every classified feed will add a field "clean_txt" which is the cleaned title + description.
    """
    def preprocessing(self):
        for lang in langs:
            for class_ in classes:
                print(f'Process: {class_} - {lang.upper()}')
                f = shopen(Utils.path_output(class_, lang), writeback=True)
                for key in f.keys():
                    f[key]['language'] = lang
                    f[key]['clean_txt'] = self.clean_feed(f[key], limit=True)
                f.close()
                print('Done.')

class DictClassifer:

    """
    Init the dict classifier.
    Assign the language, classes and create a dict.
    """
    def __init__(self, lang):
        self.lang = lang
        self.dict = {}
        self.classes = classes

    """
    Build a dict from all classes as key and 0 as value.
    """
    def build_dict_classes(self):
        ret = {}
        for class_ in self.classes:
            ret[class_] = 0
        return ret

    """
    Trains the dict classifier.
    X contains a list of clean strings.
    y is the corresponding classes.
    For every word in the string create a new key in the dict with dict_classes.
    Increments the number of apparition for a specific class of a given word.
    """
    def fit(self, X, y):
        classes_dict = self.build_dict_classes()
        for i in range(len(X)):
            for xi in X[i].split():
                if xi in self.dict.keys():
                    self.dict[xi][y[i]] += 1
                else:
                    self.dict[xi] = classes_dict.copy()

    """
    Returns the accuracy of the dict classifier.
    X contains a list of clean strings.
    y is the corresponding classes.
    Compares the list of predictions of classes with the actual classes.
    When done learn the testing set.
    """
    def score(self, X, y):
        res = 0
        size = len(X)
        pred_classes = self.predict(X)
        for i in range(size):
            if y[i] == pred_classes[i]:
                res += 1

        self.fit(X, y)
        return res / size

    """
    Predicts a list of classes from a list of clean strings.
    Use ponderation to increment a specific class (to get a relevant representation of the given class from its set).
    Each word is process only once (don't process duplicates).
    """
    def predict(self, X, min_score=None):
        dict_keys = self.dict.keys()
        lst_predict_classes = []
        done_words = []

        for x in X:
            predict_classes = self.build_dict_classes()
            for word in x.split():
                if word not in done_words:
                    done_words.append(word)
                    if word in dict_keys:
                        for key in self.dict[word].keys():
                            predict_classes[key] += self.get_ponderation(key, self.dict[word])
            # print(predict_classes)
            predict_class = max(predict_classes, key=predict_classes.get)

            if min_score is None or predict_classes[predict_class] > min_score:
                lst_predict_classes.append(predict_class)
            else:
                lst_predict_classes.append(None)

        return lst_predict_classes
    

    """
    Returns a proportion of a given class regarding its dict_classes.
    (number_representation - average_representation) / sum_representation
    """
    def get_ponderation(self, class_, dict_classes):
        lst_classes = np.asarray(list(dict_classes.values()))
        sum_ = np.sum(lst_classes)
        if sum_ > 0:
            return (dict_classes[class_] - np.average(lst_classes)) / sum_
        return 0


class Classifier:

    """
    Returns the data and the target of a vect of a given language.
    The data represents the cleaned strings.
    The target represents the corresponding classes.
    """
    def get_data_target(self, lang):
        with open(Utils.path_vect(lang), 'rb') as f:
            vect = load(f)
            data, target = [], []
            for o in vect:
                target.append(list(o.keys())[0])
                data.append(list(o.values())[0])
            return np.asarray(data), np.asarray(target)


    """
    Loads the stored classifier or create a new one if not exists.
    """
    def load_classif(self, lang):
        classif_path = Utils.path_classifier(lang)
        if os.path.exists(classif_path):
            with open(classif_path, 'rb') as f:
                return loads(load(f))

        return DictClassifer(lang)

    """
    Loads the dict_classifier and trains it.
    X contains a list of clean strings.
    y is the corresponding classes.
    Returns the dict_classifier.
    """
    def dict_classif(self, X, y, lang):
        dict_classifier = self.load_classif(lang)
        dict_classifier.fit(X, y)
        return dict_classifier

    """
    Gets the data and target and splits them into training and testing data.
    Evaluates the dict_classifier and saves it.
    """
    def classify(self):
        for lang in langs:
            data, target = self.get_data_target(lang)
            X_train, X_test, y_train, y_test = tts(data, target, test_size=0.1, random_state=0)

            clf = self.dict_classif(X_train, y_train, lang)
            score = clf.score(X_test, y_test)
            print(f'{lang.upper()} --> {self.dict_classif.__name__}: {score}')

            with open(Utils.path_classifier(lang), 'wb') as f:    
                dump(dumps(clf), f)

class Exploiter:

    """
    Creates a new dataset and preprocesses this dataset.
    """
    def update_dataset(self):
        print("Creating dataset...")
        Dataset.create_dataset()

        print("Preprocessing...")
        Cleaner().preprocessing()

        print("Done.")

    """
    Updates the dataset and trains the classifier.
    """
    def feed_dict(self):
        self.update_dataset()
        Classifier().classify()

    """
    Feed the dict classifier every 30 minutes.
    """
    def update_dict_scheduler(self):
        while True:
            self.feed_dict()
            print("Sleeping 30 min...")
            sleep(1800)

    """
    Predicts the class of a random feed.
    """
    def predict_random_feed(lang):
        feed = collect.get_random_feed(path_main_input, lang=lang)
        print(feed)

        clf = Classifier().load_classif(lang)
        clean_txt = Cleaner().clean_feed(feed, limit=True)
        print(clf.predict([clean_txt], min_score=0.4))

if __name__ == '__main__':
    # Exploiter.predict_random_feed('en')
    Exploiter().update_dict_scheduler()