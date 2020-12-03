import sys

from elasticsearch import Elasticsearch as ES
from elasticsearch.helpers import scan

from shelve import open as shopen
from json import dumps

from collector import Collector
from enrichment import Enrichment
from config import path_main_output, es_config, es_index, path_main_input, classes, langs, match_fields

collect = Collector()

class Indexer:

    """
    Add every feeds contained in the output file to an index.
    """
    def make_index(self):
        es = ES(es_config)
        es.indices.delete(index=es_index, ignore=[400, 404])
        f = shopen(path_main_output)

        print('Start indexing...')
        for key in f.keys():
            es.index(index=es_index, id=key, body=f[key])
        print('Done.')

    """
    First run the collect of the feeds.
    Then index the feeds.
    """
    def index(self, collect=True):
        if collect:
            collect.feed_parser(path_main_input, path_main_output)
        self.make_index()

class Searcher:
    
    """
    Converts the result of the query to json
    """
    def to_json(self, res):
        return list(map(lambda item: dumps(item, ensure_ascii=False), res))

    """
    Simply runs a scan with a given query
    """
    def query(self, query):
        return self.to_json(scan(ES(es_config), index=es_index, query=query))


    """
    Runs a search given multiple arguments.
    text is the string which will match some fields.
    If index is True it will index the feeds, if collect is True it will also collect them before.
    list_classes contains a list of wanted classes.
    predict_value is the minimum number of the prediction function.
    languages contains the wanted languages.
    If enrich is True, uses the word2vec vector.
    enrich_value is the confidence value of similar words.
    """
    def search(self, text=None, index=False, collect=False, list_classes=classes, predict_value=0, languages=langs, enrich=True, enrich_value=0):
        text_query = { "match_all" : {}} if text is None else { "multi_match" : { "query": text, "fields": match_fields}}
        predict_val_query = { "range": { "predict_class_val": { "gt": predict_value}}}

        if enrich and text is not None:
            enr = Enrichment()
            text_query = { "bool": { "should": [text_query]}}
            for similars in enr.most_similar(text.split()):
                for similar in similars:
                    if(similar[1] > enrich_value):
                        text_query["bool"]["should"].append({ "multi_match" : { "query": similar[0], "fields": match_fields}})

        classes_query = { "bool": { "should": []}}
        for class_ in list_classes:
            classes_query["bool"]["should"].append({ "match": { "predict_class": class_}})

        langs_query = { "bool": { "should": []}}
        for lang in languages:
            langs_query["bool"]["should"].append({ "match": { "language": lang}})

        if index:
            Indexer().index(collect=collect)

        return self.query({"query" : { "bool": { "must": [text_query, classes_query, predict_val_query, langs_query]}}})

if __name__ == '__main__':
    text = None
    index = False
    collect = False
    enrich = False
    list_classes = classes
    predict_value = 0
    enrich_value = 0
    languages = langs

    try:
        for arg in sys.argv[1:]:
            if '=' in arg:
                name, val = arg.split('=')
            
                if name == 'text':
                    text = val
                elif name == 'classes':
                    list_classes = []
                    for class_ in val.split(':'):
                        list_classes.append(class_)
                elif name == 'predict_value':
                    predict_value = float(val)
                elif name == 'enrich_value':
                    enrich_value = float(val)
                elif name == 'langs':
                    languages = []
                    for lang in val.split(':'):
                        languages.append(lang)
                else:
                    raise Exception('Unhandled name.')

            else:
                if arg == 'index':
                    index = True
                elif arg == 'collect':
                    collect = True
                elif arg == 'enrich':
                    enrich = True
                else:
                   raise Exception('Unhandled arg.') 

    except Exception as e:
        print(e)
        print("Usage: searcher (<name>=<value> || <arg>)*")

    
    res = Searcher().search(text, index=index, collect=collect, list_classes=list_classes, predict_value=predict_value, languages=languages, enrich=enrich, enrich_value=enrich_value)
    print(res)
    print(len(res))