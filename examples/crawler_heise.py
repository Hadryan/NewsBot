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

HEISE_SITES = [
    {
        "name": "heise top",
        "short": "heise",
        "rss": "https://www.heise.de/rss/heise-top-atom.xml",
        "channel_id": -1001135475495,
        "channel_link": "heise_de",
        "instant_id": -1001318200987,
        "instant_link": "http://t.me/joinchat/AAAAAE6SJpsh3C0EnOD5hw"
    },
    {
        "name": "heise online",
        "short": "ho",
        "rss": "https://www.heise.de/rss/heise-atom.xml",
        "channel_id": -1001406750046,
        "channel_link": "https://t.me/joinchat/AAAAAFPZTV5LlFEDKq3RpQ",
        "instant_id": -1001386637099,
        "instant_link": "https://t.me/joinchat/AAAAAFKmZythoHmwMbipCw"
    },
    {
        "name": "heise+",
        "short": "h+",
        "rss": "https://www.heise.de/rss/heiseplus-atom.xml",
        "channel_id": -1001168097635,
        "channel_link": "https://t.me/joinchat/AAAAAEWfwWNcay-7v8DOkw",
        "instant_id": -1001400409764,
        "instant_link": "https://t.me/joinchat/AAAAAFN4jqTYFgkhFNiSgg"
    },
    {
        "name": "heise Developer",
        "short": "hdev",
        "rss": "https://www.heise.de/developer/rss/news-atom.xml",
        "channel_id": -1001126276280,
        "channel_link": "https://t.me/joinchat/AAAAAEMhnLgx4CiOffH3ew",
        "instant_id": -1001229956264,
        "instant_link": "https://t.me/joinchat/AAAAAElPpKjBSpSOjpVZMg"
    },
    {
        "name": "heise Autos",
        "short": "hautos",
        "rss": "https://www.heise.de/autos/rss/news-atom.xml",
        "channel_id": -1001398587447,
        "channel_link": "https://t.me/joinchat/AAAAAFNcwDcZ-JUOZQjdyg",
        "instant_id": -1001287978903,
        "instant_link": "https://t.me/joinchat/AAAAAEzE_5eduSjg0bnaRA"
    },
    {
        "name": "heise Security",
        "short": "hs",
        "rss": "https://www.heise.de/security/rss/news-atom.xml",
        "channel_id": -1001269533396,
        "channel_link": "https://t.me/joinchat/AAAAAEuritSwFaAEdpRtcg",
        "instant_id": -1001337905782,
        "instant_link": "https://t.me/joinchat/AAAAAE--0nZTTneAq79YVg"
    },
    {
        "name": "c't",
        "short": "ct",
        "rss": "https://www.heise.de/ct/rss/artikel-atom.xml",
        "channel_id": -1001336077325,
        "channel_link": "https://t.me/joinchat/AAAAAE-i7A2pnSydZGlycg",
        "instant_id": -1001216824785,
        "instant_link": "https://t.me/joinchat/AAAAAEiHRdEJgcI5FrZ5sw"
    },
    {
        "name": "c't Fotografie",
        "short": "ctfoto",
        "rss": "https://www.heise.de/foto/rss/news-atom.xml",
        "channel_id": -1001249360260,
        "channel_link": "https://t.me/joinchat/AAAAAEp3uYTGVRyGKs1kfg",
        "instant_id": -1001379831032,
        "instant_link": "https://t.me/joinchat/AAAAAFI-jPgN3jxi9tHhmQ"
    },
    {
        "name": "iX",
        "short": "ix",
        "rss": "https://www.heise.de/ix/rss/news-atom.xml",
        "channel_id": -1001452361675,
        "channel_link": "https://t.me/joinchat/AAAAAFaRR8uQtKE1VxYYnw",
        "instant_id": -1001314740985,
        "instant_link": "https://t.me/joinchat/AAAAAE5dWvn2hSYGTAg9Sw"
    },
    {
        "name": "Mac & i",
        "short": "mac",
        "rss": "https://www.heise.de/mac-and-i/news-atom.xml",
        "channel_id": -1001179760234,
        "channel_link": "https://t.me/joinchat/AAAAAEZRtmqs9XmdX2V32w",
        "instant_id": -1001244446098,
        "instant_link": "https://t.me/joinchat/AAAAAEosvZL9_JXavRKlPw"
    },
    {
        "name": "Make",
        "short": "make",
        "rss": "https://www.heise.de/make/rss/hardware-hacks-atom.xml",
        "channel_id": -1001329982837,
        "channel_link": "https://t.me/joinchat/AAAAAE9F7XWJUx_nr-p3ow",
        "instant_id": -1001378368006,
        "instant_link": "https://t.me/joinchat/AAAAAFIoOgZ0eFaIQ7BGYA"
    },
    {
        "name": "Technology Review",
        "short": "tr",
        "rss": "https://www.heise.de/tr/rss/news-atom.xml",
        "channel_id": -1001185482961,
        "channel_link": "https://t.me/joinchat/AAAAAEapCNH7aIodS8A-PQ",
        "instant_id": -1001239485804,
        "instant_link": "https://t.me/joinchat/AAAAAEnhDWwCfaIgzsLFzg"
    },
]


def get_img_and_tags(link):
    source = requests.get(link).text
    img = re.findall('property="og:image" *content="([^"]+)"', source)
    tags = re.findall('name="keywords" content="([^"]+)"', source)
    img = img[0] if img else ""
    tags = tags[0].split(",") if tags else ""
    return img, tags


def main():
    for s in HEISE_SITES:
        site = Site()
        site.name = s['channel_link']
        site.alias = s['name']
        site.short = s['short']
        site.channel_id = s['channel_id']
        site.instant_id = s['instant_id']
        site.join_instant = s['instant_link']
        raw_data = feedparser.parse(s['rss'])
        for x in raw_data["entries"]:
            if site.check_article_exists(x["link"]):
                continue
            img, tags = get_img_and_tags(x["link"])
            text = x["summary"] if "summary" in x else ""
            site.add_article(
                title=x["title"], link=x["link"], text=text, tags=tags, img=img
            )
        site.post()


if __name__ == "__main__":
    main()
