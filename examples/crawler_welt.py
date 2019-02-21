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


def get_tags(link):
    sourcecode = requests.get(link).text
    tags = re.findall('name="keywords" content="([^"]*)"', sourcecode)
    tags = tags[0].split(",") if tags else tags
    return tags


def main():
    site = Site()
    site.name = "welt_de"
    site.alias = "Welt.de"
    site.short = "welt"
    site.base_url = "https://welt.de/"
    site.channel_id = -1001247567899
    site.instant_id = -1001184127734
    site.join_instant = "http://t.me/joinchat/AAAAAEaUWvabMwWbupISFw"
    raw_data = feedparser.parse("https://www.welt.de/feeds/latest.rss")
    for x in raw_data["entries"]:
        if site.check_article_exists(x["link"]):
            continue
        tags = [y["term"] for y in x["tags"]]
        img = (
            x["links"][1]["href"]
            if len(x["links"]) > 1 and x["links"][1]["type"] == "image/jpeg"
            else ""
        )
        site.add_article(
            text=x["summary"], title=x["title"], link=x["link"], tags=tags, img=img
        )
    site.post()


if __name__ == "__main__":
    main()
