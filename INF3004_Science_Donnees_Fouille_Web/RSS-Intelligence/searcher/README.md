# FEED Indexer/Searcher
## Description
Index the feeds retrieve with the collector module then allows a search with Elasticsearch module.
## Requirements
A running Elasticsearch server on localhost:9200.
The collector module.
An output folder.
## Execution
Index the feeds (this can take a while):
\>> python indexer.py
Run a search:
\>> python searcher.py <mode>
## Usability
They are 2 modes available:
  - ALL --> print all the feeds.
  - QUERY --> print only the feeds which match a given query
The query is matched with the title, description, date and language.
## Test
Display all the feeds relative to the word "Québec":
\>> python searcher.py QUERY
\>> Enter a search: Québec
