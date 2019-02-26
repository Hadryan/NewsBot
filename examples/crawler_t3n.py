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
    site.name = "t3n_de"
    site.alias = "t3n.de"
    site.short = "t3n"
    site.base_url = "https://t3n.de/"
    site.channel_id = -1001252158257
    site.instant_id = -1001452716923
    site.join_instant = "https://t.me/joinchat/AAAAAFaWs3sqBpYotA1iGw"
    raw_data = feedparser.parse("https://t3n.de/rss.xml")
    for x in raw_data["entries"]:
        if site.check_article_exists(x["link"]) or x['title'][:7] == "Anzeige":
            continue
        tags = {t['term'] for t in x['tags']}
        img_match = re.findall("<img src=\"(.*?)\"", x['summary'])
        img = img_match[0] if img_match else ""
        text = re.sub("<a(.*)</a>", "", x['summary']) if 'summary' in x else ""
        site.add_article(
            text=text, title=x["title"], link=x["link"], tags=tags, img=img
        )
    site.post()

if __name__ == "__main__":
    main()
