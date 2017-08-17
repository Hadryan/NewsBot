#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import logging
import feedparser
import html

import requests

import news
import database

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def main():
    name = 'tarnkappe'
    base_url = 'https://tarnkappe.info/'
    channel_id = -1001096556431

    check_site(name, base_url, channel_id)

    data = get_data(base_url)
    set_data(data, name, base_url)


def get_data(base_url):
    raw_data = feedparser.parse(base_url + 'feed/')
    data = []
    for x in raw_data['entries']:
        article = dict()
        article['link'] = x['link']
        text = html.unescape(x['summary'])
        article['text'] = text
        article['title'] = x['title']
        sourcecode = requests.get(article['link']).text
        img = re.findall('<meta property="og:image" content="([^"]*)"', sourcecode)[0]
        article['img'] = img
        tags = [y['term'] for y in x['tags']]
        article['tags'] = tags
        data.append(article)
    return data[::-1]


def set_data(data, name, base_url):
    for article in data:
        n = news.News(name)
        n.set_img(article['img'])
        n.set_title(article['title'])
        n.set_text(article['text'])
        n.set_link(article['link'])
        n.set_tags(article['tags'])
        n.post()


def check_site(name, link, channel_id):
    db = database.Database()
    if not db.check_site(name):
        db.insert_site(name, link)
        db.insert_channel(name, channel_id)


if __name__ == '__main__':
    main()
