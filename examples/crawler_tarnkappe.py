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
    site.name = "tarnkappe"
    site.short = "tk"
    site.alias = "Tarnkappe.info"
    site.base_url = "https://tarnkappe.info/"
    site.channel_id = -1001096556431
    site.instant_id = -1001201795584
    site.instant_hash = "ea1f50995623f3"
    site.join_instant = "http://t.me/joinchat/AAAAAEeh8gAMwazWu2hoTA"

    raw_data = feedparser.parse(site.base_url + "feed/")
    for x in raw_data["entries"]:
        if site.check_article_exists(x["link"]):
            continue
        sourcecode = requests.get(x["link"]).text
        img = re.findall('<meta property="og:image" content="([^"]*)"', sourcecode)[0]
        tags = [y["term"] for y in x["tags"]]
        site.add_article(
            link=x["link"], title=x["title"], text=x["summary"], img=img, tags=tags
        )
    site.post()


if __name__ == "__main__":
    main()
