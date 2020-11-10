import sys

from elasticsearch import Elasticsearch as ES
from elasticsearch.helpers import scan

from shelve import open as shopen
from json import dumps

from collector import Collector
from config import op_path, es_config, es_index, path_main_input

collect = Collector()

class Indexer:

    """
    Add every feeds contained in the output file to an index.
    """
    def make_index(self):
        es = ES(es_config)
        es.indices.delete(index=es_index, ignore=[400, 404])
        f = shopen(op_path)

        print('Start indexing...')
        for key in f.keys():
            es.index(index=es_index, id=key, body=f[key])
        print('Done.')

    """
    First run the collect of the feeds.
    Then index the feeds.
    """
    def index(self):
        collect.feed_parser(path_main_input, op_path)
        self.make_index()

class Searcher:
    
    """
    Parse the item into JSON then print it
    """
    def print_item(self, res):
        for item in res:
            print(dumps(item, ensure_ascii=False))

    """
    Get every item of the index
    """
    def get_all(self):
        es = ES(es_config)
        res = scan(es, index=es_index, query={"query": { "match_all" : {}}})
        self.print_item(res)

    """
    Ask the user a word to query
    Run a search and get every item which match the given query
    """
    def get_query(self):
        query = input("Enter a search: ")
        es = ES(es_config)
        req = {
        "query": {
            "multi_match" : {
            "query": query,
            "fields": ["title", "language", "date", "description"]
            }
        }
        }
        res = scan(es, index=es_index, query=req)
        self.print_item(res)

    """
    Handle the given mode
    """
    def search(self, mode, index=False):
        if index:
            Indexer().index()
        if mode == 'ALL':
            self.get_all()
        elif mode == 'QUERY':
            self.get_query()
        else:
            print(f'Unhandled mode {mode}')

if __name__ == '__main__':
    try:
        Searcher().search(sys.argv[1], index=True)
    except Exception as e:
        print(e)
        print("Usage: searcher <mode>")