#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

import html
import logging
import re

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
    site.name = "heise_de"
    site.alias = "Heise.de"
    site.short = "heise"
    site.base_url = "https://heise.de/"
    site.channel_id = -1001135475495
    raw_data = feedparser.parse("https://www.heise.de/newsticker/heise-atom.xml")
    for x in raw_data["entries"]:
        img = re.findall('<img src="([^"]*)"', x["content"][0]["value"])
        if img:
            img = img[0]
            img = re.sub("scale/geometry/([^/]*)/", "scale/geometry/720/", img)
        tags = get_tags(x["link"])
        site.add_article(
            text=x["summary"],
            title=x["title"],
            link=x["link"],
            img=img if img else "",
            tags=tags,
        )
    site.post()


if __name__ == "__main__":
    main()
