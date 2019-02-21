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
    site.name = "spiegelde"
    site.alias = "spiegel-online"
    site.short = "spiegel"
    site.base_url = "https://spiegel-online.de/"
    site.channel_id = -1001442405890
    site.instant_id = -1001182811341
    site.join_instant = "http://t.me/joinchat/AAAAAEaARM11yh3ZtMJGXQ"
    raw_data = feedparser.parse("http://www.spiegel.de/schlagzeilen/index.rss")
    for x in raw_data["entries"]:
        if site.check_article_exists(x["link"]):
            continue
        img, tags = get_img_and_tags(x["link"])
        site.add_article(
            text=x["summary"], title=x["title"], link=x["link"], tags=tags, img=img
        )
    site.post()


def get_img_and_tags(link):
    source = requests.get(link).text
    img = re.findall('property="og:image" *content="([^"]+)"', source)
    tags = re.findall('name="news_keywords" content="([^"]+)"', source)
    img = img[0] if img else ""
    tags = tags[0].split(",") if tags else ""
    return img, tags


if __name__ == "__main__":
    main()
