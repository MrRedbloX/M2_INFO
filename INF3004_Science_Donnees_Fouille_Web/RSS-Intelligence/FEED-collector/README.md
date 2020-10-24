# FEED Collector
## Description
Collect all the most recent feeds from a list of url and save the result in a file.
## Requirements
A folder input needs to contain a file urls.txt which has a list of urls for rss feeds.
A folder output which will contain after execution a file feeds.data.
## Execution
Run in a terminal:
\>> python feed_parser.py
## Usability
Exploit the content of feeds.data using the function load from the pickle librairy.
The result will be a list.
## Test
Display the raw content of feed.data by using:
\>> python print_raw_feeds.py
