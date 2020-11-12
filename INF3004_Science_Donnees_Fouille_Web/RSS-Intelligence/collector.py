from feedparser import parse
from langdetect import detect
from hashlib import md5
from bs4 import BeautifulSoup as bs
from shelve import open as shopen
from random import choice

class Collector:

    """
    Collect feeds from a url.
    Return a list of dict representing a feed.
    A feed has: a title, a source url and page, the language of the post, a unique id and eventually a published date + a description.
    If the url is not valid it returns an empty list.
    """
    def collect(self, url):
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
    Store the feeds in local file.
    Takes a list of feeds and store each feed in a file accessible by a unique key.
    """
    def store(self, filename, feeds):
        f = shopen(filename)
        f.clear()
        for feed in feeds:
            key = feed['id']
            del feed['id']
            f[key] = feed
        f.close()

    """
    First it retrieves a list of urls which point to rss feeds.
    Then it collects all the feeds in a list.
    Finally it dumps the list into a file.
    """
    def feed_parser(self, urls, output):
        urls = open(urls, 'r').read().splitlines()
        feeds = []

        print('Start collecting feeds...')
        for url in urls:
            feeds.extend(self.collect(url))
        print('Done.')

        self.store(output, feeds)

    """
    From a list of urls and eventually a specific language return a random feed
    """
    def get_random_feed(self, urls, lang=None):
        lst_urls = open(urls, 'r').read().splitlines()
        while True:
            url = choice(lst_urls)
            collected = self.collect(url)
            if len(collected) > 0:
                ret = choice(collected)
                if lang is None or ret['language'] == lang:    
                    return ret
            lst_urls.remove(url)
            if len(urls) == 0:
                raise Exception('No more urls available')