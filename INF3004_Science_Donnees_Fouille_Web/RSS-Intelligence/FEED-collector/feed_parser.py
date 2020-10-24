"""
All of external librairies used are free of re-use for personnal or professional purposes.
"""
from feedparser import parse
from langdetect import detect
from hashlib import md5
from bs4 import BeautifulSoup as bs
from pickle import dump

"""
Collect feeds from a url.
Return a list of dict representing a feed.
A feed has: a title, a source url and page, the language of the post, a unique id and eventually a published date + a description
If the url is not valid it returns an empty list
"""
def collect(url):
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
            process['description'] = ''.join(bs(post['summary'], features='lxml').findAll(text=True))
        collector.append(process)
    return collector

"""
The main execution of feed parser.
First it retrieves a list of urls which point to rss feeds.
Then it collects all the feeds in a list.
Finally it dumps the list into a file.
"""
if __name__ == '__main__':
    urls = open('input/urls.txt', 'r').read().splitlines()
    attributes = [('source_page', 'link'), ('date', 'published'), ('description', 'summary')]
    results = []

    print('Start collecting feeds...')
    for url in urls:
        results.extend(collect(url))
    print('Done.')

    with open('./output/feeds.data', 'wb') as f:
        dump(results, f)
