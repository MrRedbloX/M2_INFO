langs = ['en', 'fr'] # Languages for the classifier
classes = ['ART_CULTURE', 'ECONOMIE', 'POLITIQUE', 'SANTE_MEDECINE', 'SCIENCE', 'SPORT'] # Predict classes for the classifier
path_res = './res' # Path to the ressource file
path_main_input = './input/urls.txt' # Path to the main input file
path_main_output = './output/feeds' # Path to the main output shelve
es_config = [{'host': 'localhost', 'port': 9200}] # Configuration for ElasticSearch server
es_index = 'feeds' # Index of feeds for ElasticSearch
match_fields = ["title", "language", "date", "description", "text"] # The fields used to match a search