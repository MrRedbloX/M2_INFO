from feedparser import parse
from langdetect import detect
from hashlib import md5
from bs4 import BeautifulSoup as bs

def collect(url):
    def clean(elt):
        return ''.join(bs(elt, features='lxml').findAll(text=True))

    try:
        entries = parse(url).entries
    except:
        print(f'URL `{url}` is not valid.')
        return []
    collector = []
    for post in entries:
        process = {}
        process['title'] = post['title']
        process['source_url'] = url
        process['language'] = detect(process['title'])
        process['source_page'] = post['link']
        process['id'] = md5(str(process['title']+process['source_url']+process['language']+process['source_page']).encode()).hexdigest()
        process['date'] = None
        if 'published' in post:
            process['date'] = post['published']
        process['description'] = None
        if 'summary' in post:
            process['description'] = clean(post['summary'])
        collector.append(process)
    return collector

if __name__ == '__main__':
    urls = open('input/urls.txt', 'r').read().splitlines()
    attributes = [('source_page', 'link'), ('date', 'published'), ('description', 'summary')]
    results = []

    for url in urls:
        results.extend(collect(url))
    print(results)
