import sys
from elasticsearch import Elasticsearch as ES
from elasticsearch.helpers import scan
from json import dumps
from config import *


"""
Parse the item into JSON then print it
"""
def print_item(res):
    for item in res:
        print(dumps(item, ensure_ascii=False))

"""
Get every item of the index
"""
def get_all():
    es = ES(es_config)
    res = scan(es, index=es_index, query={"query": { "match_all" : {}}})
    print_item(res)

"""
Ask the user a word to query
Run a search and get every item which match the given query
"""
def get_query():
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
    print_item(res)

"""
Handle the given mode
"""
def searcher(mode):
    if mode == 'ALL':
        get_all()
    elif mode == 'QUERY':
        get_query()
    else:
        print(f'Unhandled mode {mode}')

if __name__ == '__main__':
    try:
        searcher(sys.argv[1])
    except Exception as e:
        print(e)
        print("Usage: searcher <mode>")
