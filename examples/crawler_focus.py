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
    site.name = "focus_online"
    site.alias = "FOCUS Online"
    site.short = "focus"
    site.base_url = "https://www.focus.de/"
    site.channel_id = -1001317811798
    for x in feedparser.parse(
        "https://rss.focus.de/fol/XML/rss_folnews_eilmeldungen.xml"
    )["entries"]:
        link = x["link"]
        text = x["summary"]
        text = re.split("\n", text, re.MULTILINE)
        text = html.unescape(text[-1].split("<br />")[0])
        img = get_img(link)
        tags = [y["term"] for y in x["tags"]]
        title = html.unescape(x["title"])
        site.add_article(title=title, text=text, link=link, img=img, tags=tags)
    site.post()


def get_img(link):
    response = requests.get(link)
    img = re.findall('<meta content="([^"]+)" property="twitter:image"/', response.text)
    return img[0] if img else ""


if __name__ == "__main__":
    main()
