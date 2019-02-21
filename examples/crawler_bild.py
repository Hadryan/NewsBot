#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

import logging
import re

import feedparser

from telegramnews import Site

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def main():
    site = Site()
    site.name = "bild_de"
    site.alias = "Bild.de"
    site.short = "bild"
    site.base_url = "http://www.bild.de/"
    site.channel_id = -1001142790377
    site.instant_id = -1001458030907
    site.join_instant = "http://t.me/joinchat/AAAAAFbnyTtakCsqpHNi8g"
    for x in feedparser.parse(
        "http://www.bild.de/rssfeeds/vw-news/vw-news-16726644,sort=1,view=rss2.bild.xml"
    )["entries"]:
        text = x["summary"]
        text = re.split("\n", text, re.MULTILINE)
        text = text[-1].split("<br />")[0]
        img = (
            x["media_thumbnail"][0]["url"].replace(",w=120,", ",w=1200,")
            if "media_thumbnail" in x
            else None
        )
        tags = [y["term"] for y in x["tags"]]
        site.add_article(
            title=x["title"], text=text, link=x["link"], img=img, tags=tags
        )
    site.post()


if __name__ == "__main__":
    main()
