from feed_parser import feed_parser

"""
Refresh the feeds every 5 minutes.
Calls feed_parser on a regular basis to update the feeds.
"""
def feed_scheduler(urls, output):
    while True:
        feed_parser(urls, output)
        sleep(300)

if __name__ == '__main__':
    feed_scheduler('input/urls.txt', './output/feeds')
