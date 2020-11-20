# RSS-Intelligence
Internet watch system which exploits RSS feeds.
## Collector module
Collects and stores feeds from RSS feed urls.
## Searcher module
### Indexer
Indexes collected feeds with ElasticSearch module.
### Searcher
Allows to run a seach on indexed feeds.
Here are some examples:  
\>> python searcher.py classes=POLITIQUE:SCIENCE text=biden predict_value=0.1  
\>> python searcher.py index classes=POLITIQUE:SCIENCE text=trump  
\>> python searcher.py index collect text="New York" langs=en  
## Classifier module
Predicts a class for a given feed.
### Dataset
From a list of relevant urls corresponding to a specific class, creates a dataset for each handled class and language.
### Cleaning
For every feed in the dataset, creates a string with the cleaned title and description.
### Dictionnary Classifier
From a list of feeds to learn and their corresponding classes, learns the data and is able to predict a class for a new feed.
### Exploitation
Feed the Dictionnary Classifier (create dataset, preprocessing, ...) or predicts the class of a random feed.
## Enrichment module
Uses Word2Vec lib to get better understanding of word proximity for the Searcher module.