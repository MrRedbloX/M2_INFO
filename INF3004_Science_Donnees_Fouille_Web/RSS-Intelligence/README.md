# RSS-Intelligence
Internet watch system which exploits RSS feeds.
## Collector module
Collects and stores feeds from RSS feed urls.
## Searcher module
### Indexer
Indexes collected feeds with ElasticSearch module.
### Searcher
Allows to run a seach on indexed feeds.
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