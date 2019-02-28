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
    site.name = "rundschau"
    site.alias = "Frankfurter Rundschau"
    site.short = "fr"
    site.base_url = "https://fr.de/"
    site.channel_id = -1001389663056
    raw_data = feedparser.parse("https://www.fr.de/rssfeed.rdf")
    for x in raw_data["entries"]:
        if site.check_article_exists(x["link"]):
            continue
        img, tags = get_img_and_tags(x["link"])
        text = x["summary"] if 'summary' in x else ''
        site.add_article(
            text=text, title=x["title"], link=x["link"], tags=tags, img=img
        )
    site.post()


def get_img_and_tags(link):
    source = requests.get(link).text
    img = re.findall('content="([^"]+)" *property="og:image"', source)
    tags = re.findall("dimension3: '([^']*)', ", source)
    img = img[0] if img else ""
    tags = tags[0].split("|") if tags else ""
    return img, [t for t in tags if t not in ['fr']]


if __name__ == "__main__":
    main()
