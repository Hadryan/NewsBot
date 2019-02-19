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
    site.name = "welt_de"
    site.alias = "Welt.de"
    site.short = "welt"
    site.base_url = "https://welt.de/"
    site.channel_id = -1001135475495
    raw_data = feedparser.parse("https://www.welt.de/feeds/latest.rss")
    for x in raw_data["entries"]:
        text = html.unescape(x["summary"])
        title = html.unescape(x["title"])
        tags = [y["term"] for y in x["tags"]]
        img = x['links'][1]['href'] if len(x['links']) > 1 and x['links'][1]['type'] == 'image/jpeg' else ""
        site.add_article(
            text=text, title=title, link=x["link"], tags=tags, img=img
        )
    site.post()


if __name__ == "__main__":
    main()
