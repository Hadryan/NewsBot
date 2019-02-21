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


def main():
    site = Site()
    site.name = "golem_de"
    site.alias = "Golem.de"
    site.short = "golem"
    site.base_url = "https://golem.de/"
    site.channel_id = -1001138540100
    site.instant_id = -1001304871255
    site.join_instant = "http://t.me/joinchat/AAAAAE3GwVcigPpRU96awA"
    for x in feedparser.parse("https://rss.golem.de/rss.php?feed=RSS2.0")["entries"]:
        text = x["summary"].split("(<a")[0]
        article_code = requests.get(x["link"]).text
        img = re.findall(
            '"twitter:image" property="og:image" content="([^"]*)"', article_code
        )[0]
        tags = re.findall('a href="[^"]*">([^<]*)<', html.unescape(x["summary"]))
        site.add_article(
            text=text, title=x["title"], img=img, tags=tags, link=x["link"]
        )
    site.post()


if __name__ == "__main__":
    main()
