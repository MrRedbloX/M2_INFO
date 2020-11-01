"""
Necessary in order to access the collector module
"""
import sys
sys.path.append('../')

from elasticsearch import Elasticsearch as ES
from shelve import open as shopen
from collector.feed_parser import feed_parser as fp
from config import *


"""
Add every feeds contained in the output file to an index.
"""
def make_index():
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
def indexer():
    fp('../collector/input/urls.txt', op_path)
    make_index()

if __name__ == '__main__':
    indexer()
