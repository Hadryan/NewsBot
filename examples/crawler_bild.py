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

BILD_SITES = [

    {
        "name": "Bild Top News",
        "short": "bild",
        "rss": "https://www.bild.de/rss-feeds/rss-16725492,feed=Newsticker.bild.html",
        "channel_id": -1001142790377,
        "channel_link": "bild_de",
        "instant_id": -1001458030907,
        "instant_link": "http://t.me/joinchat/AAAAAFbnyTtakCsqpHNi8g"
    },
    {
        "name": "Bild All News",
        "short": "bn",
        "rss": "https://www.bild.de/rss-feeds/rss-16725492,feed=news.bild.html",
        "channel_id": -1001428043294,
        "channel_link": "https://t.me/joinchat/AAAAAFUeNh5peUi4tfuzaw",
        "instant_id": -1001367639041,
        "instant_link": "https://t.me/joinchat/AAAAAFGEhAGu4PN6yg-hJw",
    },
    {
        "name": "Bild Sport News",
        "short": "bsn",
        "rss": "https://www.bild.de/rss-feeds/rss-16725492,feed=sport.bild.html",
        "channel_id": -1001123620781,
        "channel_link": "https://t.me/joinchat/AAAAAEL5F63ZtNguUo7rJA",
        "instant_id": -1001168953180,
        "instant_link": "https://t.me/joinchat/AAAAAEWsz1zLIXiE5qGXVw",
    },
    {
        "name": "Bild Politik News",
        "short": "bpn",
        "rss": "https://www.bild.de/rss-feeds/rss-16725492,feed=politik.bild.html",
        "channel_id": -1001245121999,
        "channel_link": "https://t.me/joinchat/AAAAAEo3Dc8GQKV9w0V6bw",
        "instant_id": -1001422796576,
        "instant_link": "https://t.me/joinchat/AAAAAFTOJyDl7HrKAWXZwQ",
    },
    {
        "name": "Bild Auto News",
        "short": "ban",
        "rss": "https://www.bild.de/rss-feeds/rss-16725492,feed=auto.bild.html",
        "channel_id": -1001327029924,
        "channel_link": "https://t.me/joinchat/AAAAAE8Y3qRcWKS8GKqaWA",
        "instant_id": -1001284389344,
        "instant_link": "https://t.me/joinchat/AAAAAEyOOeDW14qxubKP1w",
    },
]


def main():
    for s in BILD_SITES:
        site = Site()
        site.name = s['channel_link']
        site.alias = s['name']
        site.short = s['short']
        site.channel_id = s['channel_id']
        site.instant_id = s['instant_id']
        site.join_instant = s['instant_link']
        for x in feedparser.parse(s['rss'])["entries"]:
            if site.check_article_exists(x["link"]):
                continue
            text = ""
            if "summary" in x:
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
