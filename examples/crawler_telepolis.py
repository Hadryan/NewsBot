#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import logging

import feedparser

from telegramnews import Site

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def main():
    site = Site()
    site.name = "telepolis_de"
    site.alias = "Telepolis.de"
    site.base_url = "https://heise.de/tp"
    site.channel_id = -1001128692603
    site.instant_id = -1001342689984
    site.join_instant = "http://t.me/joinchat/AAAAAFAH0sBMP7A7NMf0xw"

    raw_data = feedparser.parse("https://www.heise.de/tp/news-atom.xml")
    for x in raw_data["entries"]:
        if site.check_article_exists(x["link"]):
            continue
        site.add_article(title=x["title"], link=x["link"], text=x["summary"])
    site.post(1)


if __name__ == "__main__":
    main()
