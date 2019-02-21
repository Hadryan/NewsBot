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
    site.name = "focus_online"
    site.alias = "FOCUS Online"
    site.short = "focus"
    site.base_url = "https://www.focus.de/"
    site.channel_id = -1001358620859
    for x in feedparser.parse(
        "https://rss.focus.de/fol/XML/rss_folnews_eilmeldungen.xml"
    )["entries"]:
        link = x["link"]
        text = x["summary"]
        text = re.split("\n", text, re.MULTILINE)
        text = text[-1].split("<br />")[0]
        img = get_img(link)
        tags = [y["term"] for y in x["tags"]]
        site.add_article(title=x["title"], text=text, link=link, img=img, tags=tags)
    site.post()


def get_img(link):
    response = requests.get(link)
    img = re.findall('<meta content="([^"]+)" property="twitter:image"/', response.text)
    return img[0] if img else ""


if __name__ == "__main__":
    main()
