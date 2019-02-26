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
    site.name = "pro_linux_de"
    site.alias = "Pro-Linux.de"
    site.short = "proli"
    site.base_url = "https://www.pro-linux.de/"
    site.channel_id = -1001232676629
    site.instant_id = -1001499098018
    site.join_instant = "https://t.me/joinchat/AAAAAFlaa6IhIGAqmFuZFQ"
    raw_data = feedparser.parse("https://www.pro-linux.de/NB3/rss/2/4/atom_aktuell.xml")
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
    tags = re.findall('<h3 class="topic">(.*)</h3>', source)
    img = img[0] if img else ""
    tags = tags[0].split("::") if tags else ""
    return img, tags


if __name__ == "__main__":
    main()
