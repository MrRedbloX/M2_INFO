langs = ['en', 'fr']
classes = ['ART_CULTURE', 'ECONOMIE', 'POLITIQUE', 'SANTE_MEDECINE', 'SCIENCE', 'SPORT']
path_res = './res'
path_main_input = './input/urls.txt'
path_main_output = './output/feeds'
es_config = [{'host': 'localhost', 'port': 9200}]
es_index = 'feeds'
match_fields = ["title", "language", "date", "description"]