#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

import html
import logging
import re
import shlex

import feedparser
import requests

from telegramnews import Site

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def get_img_and_tags(link):
    source = requests.get(link).text
    img = re.findall('property="og:image" *content="([^"]+)"', source)
    tags = re.findall("var tags = '([^']+)'", source)
    img = img[0] if img else ""
    tags = shlex.split(tags[0].replace("|", " "))
    return img, tags


def main():
    site = Site()
    site.name = "tagesthemen_de"
    site.alias = "tagesschau.de"
    site.short = "tages"
    site.base_url = "https://www.tagesschau.de/xml/rss2"
    site.channel_id = -1001151817211
    site.instant_id = -1001450868426
    site.join_instant = "http://t.me/joinchat/AAAAAFZ6fsojLN6G1q2rmA"
    raw_data = feedparser.parse("https://www.tagesschau.de/xml/atom/")
    for x in raw_data["entries"]:
        if x["link"] in [
            "https://novi.funk.net",
            "http://blog.ard-hauptstadtstudio.de",
        ]:
            continue
        if site.check_article_exists(x["link"]):
            continue
        img, tags = get_img_and_tags(x["link"])
        site.add_article(
            text=x["summary"], title=x["title"], link=x["link"], tags=tags, img=img
        )
    site.post()


if __name__ == "__main__":
    main()
