#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    site.name = "tarnkappe"
    site.short = "tk"
    site.alias = "Tarnkappe.info"
    site.base_url = "https://tarnkappe.info/"
    site.channel_id = -1001096556431

    raw_data = feedparser.parse(site.base_url + "feed/")
    for x in raw_data["entries"]:
        text = x["summary"]
        sourcecode = requests.get(x["link"]).text
        img = re.findall('<meta property="og:image" content="([^"]*)"', sourcecode)[0]
        tags = [y["term"] for y in x["tags"]]
        site.add_article(
            link=x["link"], title=x["title"], text=text, img=img, tags=tags
        )
    site.post()


if __name__ == "__main__":
    main()
