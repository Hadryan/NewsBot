#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
import logging
from pprint import pprint

import feedparser
import html
import news
import database

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def main():
    name = 'telepolis_de'
    alias = 'Telepolis.de'
    base_url = 'https://heise.de/tp'
    channel_id = -1001128692603

    check_site(name, alias, base_url, channel_id)

    data = get_data()
    set_data(data, name)


def get_data():
    raw_data = feedparser.parse('https://www.heise.de/tp/news-atom.xml')
    data = []
    for x in raw_data['entries']:
        article = dict()
        article['link'] = x['link']
        text = html.unescape(x['summary'])
        article['text'] = text
        title = html.unescape(x['title'])
        article['title'] = title
        data.append(article)
    return data[::-1]


def set_data(data, name):
    for article in data:
        n = news.News(name)
        n.set_title(article['title'])
        n.set_text(article['text'])
        n.set_link(article['link'])
        n.set_variante(3)
        n.post()


def check_site(name, alias, link, channel_id):
    db = database.Database()
    if not db.check_site(name):
        db.insert_site(name, alias, link)
        db.insert_channel(name, channel_id)


if __name__ == '__main__':
    main()
