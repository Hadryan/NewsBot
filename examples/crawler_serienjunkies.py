#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

import logging
import re

import feedparser
import requests

from telegramnews import Site

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def main():
    site = Site()
    site.name = "serienjunkies"
    site.alias = "serienjunkies"
    site.short = "sj"
    site.base_url = "https://serienjunkies.de"
    site.channel_id = -1001422493025
    raw_data = feedparser.parse("https://www.serienjunkies.de/rss/news.xml")
    for x in raw_data["entries"]:
        link_match = re.findall("(.*\.html)", x['link'])
        link = link_match[0] if link_match else x['link']
        if site.check_article_exists(link):
            continue
        img, tags = get_img_and_tags(x["link"])
        site.add_article(
            text=x["summary"], title=x["title"], link=link, tags=tags, img=img
        )
    site.post()


def get_img_and_tags(link):
    r = requests.get(link)
    r.encoding = "utf-8"
    source = r.text
    img = re.findall('property="og:image" *content="([^"]+)"', source)
    tags = re.findall('name="news_keywords" content="([^"]+)"', source)
    img = img[0] if img else ""
    tags = tags[0].split(",") if tags else ""
    return img, tags


if __name__ == "__main__":
    main()
