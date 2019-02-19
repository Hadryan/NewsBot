#!/usr/bin/env python
# -*- coding: utf-8 -*-


import html
import logging
import re
from pprint import pprint

import feedparser
import requests

from telegramnews import Site

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def get_tags(link):
    sourcecode = requests.get(link).text
    tags = re.findall('name="keywords" content="([^"]*)"', sourcecode)
    tags = tags[0].split(",") if tags else tags
    return tags


def main():
    site = Site()
    site.name = "spiegelde"
    site.alias = "spiegel-online"
    site.short = "spiegel"
    site.base_url = "https://spiegel-online.de/"
    site.channel_id = -1001135475495
    raw_data = feedparser.parse("http://www.spiegel.de/schlagzeilen/index.rss")
    for x in raw_data["entries"]:
        pprint(x)
        text = html.unescape(x["summary"]) if "summary" in x else ""
        title = html.unescape(x["title"])
        img, tags = get_img_and_tags(x["link"])
        site.add_article(
            text=text, title=title, link=x["link"], tags=tags, img=img
        )
    site.post()


def get_img_and_tags(link):
    source = requests.get(link).text
    img = re.findall("property=\"og:image\" *content=\"([^\"]+)\"", source)
    tags = re.findall("name=\"news_keywords\" content=\"([^\"]+)\"", source)
    img = img[0] if img else ""
    tags = tags[0].split(",") if tags else ""
    return img, tags


if __name__ == "__main__":
    main()
