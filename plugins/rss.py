from bs4 import BeautifulSoup
from bs4.element import Comment
import pandas as pd
import numpy as np
import requests

feed_url = "https://indiankanoon.org/feeds/latest/"
blog_feed = feedparser.parse(feed_url)
blog_feed.feed.title

blog_feed.feed.link
len(blog_feed.entries)

print(blog_feed.entries[0].title)
print(blog_feed.entries[0].description)

tags = [tag.term for tag in blog_feed.entries[0].tags]
authors = [author.name for author in blog_feed.entries[0].authors]
final_data = pd.DataFrame()
for i in range(10):

    url = "".format(i + 1)

    xml_data = requests.get(url).content

    soup = BeautifulSoup(xml_data, "xml")

    texts = str(soup.findAll(text=True)).replace('\\n', '')

    child = soup.find("entry")

    Title = []
    content_type = []
    updated = []
    rating = []
    user_name = []

    while True:
        try:
            updated.append(" ".join(child.find('updated')))
        except:
            updated.append(" ")

        try:
            Title.append(" ".join(child.find('title')))
        except:
            Title.append(" ")

        try:
            content_type.append(" ".join(child.find('content')))
        except:
            content_type.append(" ")

        try:
            rating.append(" ".join(child.find('im:rating')))
        except:
            rating.append(" ")

        try:
            user_name.append(" ".join(child.find('name')))
        except:
            user_name.append(" ")

        try:
            # Next sibling of child, here: entry
            child = child.find_next_sibling('entry')
        except:
            break