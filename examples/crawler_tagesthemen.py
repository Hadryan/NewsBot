#!/usr/bin/env python
# -*- coding: utf-8 -*-


import html
import logging
import re
import shlex
from pprint import pprint

import feedparser
import requests


from telegramnews import Site

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

def get_img_and_tags(link):
    source = requests.get(link, verify = False).text
    img = re.findall("property=\"og:image\" *content=\"([^\"]+)\"", source)
    tags = re.findall("var tags = '([^']+)'", source)
    img = img[0] if img else ""
    tags = shlex.split(tags[0].replace("|", " "))
    return img, tags


def main():
    site = Site()
    site.name = "tagesschau"
    site.alias = "tagesschau.de"
    site.short = "tages"
    site.base_url = "https://www.tagesschau.de/xml/rss2"
    site.channel_id = -1001135475495
    raw_data = feedparser.parse("https://www.tagesschau.de/xml/atom/")
    for x in raw_data["entries"]:
        if x['link'] in ['https://novi.funk.net', 'http://blog.ard-hauptstadtstudio.de']:
            continue
        text = html.unescape(x["summary"])
        title = html.unescape(x["title"])
        img, tags = get_img_and_tags(x['link'])
        site.add_article(
            text=text, title=title, link=x["link"], tags=tags, img=img
        )
    site.post()


if __name__ == "__main__":
    main()
