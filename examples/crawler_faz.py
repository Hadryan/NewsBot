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

from telegramnews.news_site import Site

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def main():
    site = Site()
    site.name = "faz_net"
    site.alias = "Frankfurter Allgemeine"
    site.short = "faz"
    site.base_url = "https://faz.net/"
    site.channel_id = -1001430790847
    raw_data = feedparser.parse("https://www.faz.net/rss/aktuell/")
    for x in raw_data["entries"]:
        text = (
            html.unescape(re.findall("<p>.*</p>", x["summary"])[0])
            if "summary" in x
            else ""
        )
        img, tags = get_img_and_tags(x["link"])
        site.add_article(
            text=text, title=x["title"], link=x["link"], img=img, tags=tags
        )
    site.post()


def get_img_and_tags(link):
    source = requests.get(link).text
    img = re.findall('property="og:image" *content="([^"]+)"', source)
    tags = re.findall('name="keywords" content="([^"]+)"', source)
    img = img[0] if img else ""
    tags = tags[0].split(",") if tags else ""
    return img, tags


if __name__ == "__main__":
    main()
