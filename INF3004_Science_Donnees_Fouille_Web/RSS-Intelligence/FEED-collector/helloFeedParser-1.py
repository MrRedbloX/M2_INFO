#!/usr/bin/python3


#

import urllib.request, feedparser


proxy = urllib.request.ProxyHandler({'http' : 'http://squidva.univ-ubs.fr:3128/'} )

import time
from subprocess import check_output

# ------
# uptime
# ------

uptime = check_output(['uptime'])
print("\n")
print('-------------------------------------------------------------')
print(uptime.strip())
print('-------------------------------------------------------------')
print("\n")


# --------------------
# CNN Collector (feedparser)
# --------------------

d = feedparser.parse("http://rss.cnn.com/rss/edition.rss", handlers = [proxy])

# print all posts
count = 1
blockcount = 1
for post in d.entries:
    if count % 5 == 1:
        print("\n" + time.strftime("%a, %b %d %I:%M %p") + '  ((( CNN - ' + str(blockcount) + ' )))')
        print("-----------------------------------------\n")
        blockcount += 1
    print(post.title + "\n")
    count += 1
