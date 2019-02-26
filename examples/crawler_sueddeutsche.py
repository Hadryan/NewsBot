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
    site.name = "sueddeutsche"
    site.alias = "Süddeutsche"
    site.short = "sz"
    site.base_url = "https://sueddeutsche.de/"
    site.channel_id = -1001356683060
    site.instant_id = -1001431408008
    site.join_instant = "https://t.me/joinchat/AAAAAFVRjYiqwgQUBJvWqQ"
    raw_data = feedparser.parse("https://rss.sueddeutsche.de/rss/Topthemen")
    for x in raw_data["entries"]:
        img, tags = get_img_and_tags(x["link"])
        site.add_article(
            text=x["summary"], title=x["title"], link=x["link"], img=img, tags=tags
        )
    site.post()


def get_img_and_tags(link):
    source = requests.get(link).text
    img = re.findall('property="og:image" *content="([^"]+)"', source)
    tags = re.findall('name="keywords" content="([^"]+)"', source)
    img = img[0] if img else ""
    tags = tags[0] if tags else ""
    tags = tags.replace("S&uuml;ddeutsche Zeitung Sport", "").replace("Sport", "").replace("S&uuml;ddeutsche Zeitung",
                                                                                           "").replace("SZ", "")
    tags = re.findall("^(.*?)[, ]*$", tags)
    tags = tags[0] if tags else ""
    return img, tags.split(",")


if __name__ == "__main__":
    main()
