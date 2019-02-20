#!/usr/bin/env python
# -*- coding: utf-8 -*-


import html
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

    raw_data = feedparser.parse("https://www.heise.de/tp/news-atom.xml")
    for x in raw_data["entries"]:
        site.add_article(title=x["title"], link=x["link"], text=x["summary"])
    site.post(1)


if __name__ == "__main__":
    main()
