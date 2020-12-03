# RSS-Intelligence
Internet watch system which exploits RSS feeds.
## Modules
### Collector
Collects and stores feeds from RSS feed urls.
### Searcher
#### Indexer
Indexes collected feeds with ElasticSearch module.
#### Searcher
Allows to run a seach on indexed feeds (see examples below). 
### Classifier
Predicts a class for a given feed.
#### Dataset
From a list of relevant urls corresponding to a specific class, creates a dataset for each handled class and language.
#### Cleaning
For every feed in the dataset, creates a string with the cleaned title and description.
#### Dictionnary Classifier
From a list of feeds to learn and their corresponding classes, learns the data and is able to predict a class for a new feed.
#### Exploitation
Feed the Dictionnary Classifier (create dataset, preprocessing, ...) or predicts the class of a random feed.
### Enrichment
Uses Word2Vec lib to get better understanding of word proximity for the Searcher module.

*For more details, check code documentation.*
## Architecture
In order to work properly, the following directory structure is needed at the root of the project:

input  
output  
res  
├───classifier  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├───en  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└───fr  
├───data  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├───ART_CULTURE  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├───en  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├───input  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└───output  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└───fr  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├───input  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└───output   
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├───ECONOMIE  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;. . .  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.  
├───enrich  
└───vect  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├───en  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└───fr  

More languages can be added.
## Examples
Predict a random english feed:
> python classifier.py predict_random_feed en

Schedule the training of the classifier:
> python classifier.py update_dict_scheduler

Search Donald Trump only on french feeds with ART_CULTURE and SPORT classes:
> python seacher.py text="Donald Trump" langs=fr classes=ART_CULTURE:SPORT

Search Maradona with the collect, index and a confident prediction:
> python searcher.py text=Maradona collect index predict_value=0.7