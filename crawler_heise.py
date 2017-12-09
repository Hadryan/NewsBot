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
    name = 'heise_de'
    alias = 'Heise.de'
    base_url = 'https://heise.de/'
    channel_id = -1001135475495

    check_site(name, alias, base_url, channel_id)

    data = get_data()
    set_data(data, name)


def get_data():
    raw_data = feedparser.parse('https://www.heise.de/newsticker/heise-atom.xml')
    data = []
    for x in raw_data['entries']:
        article = dict()
        article['link'] = x['link']
        text = html.unescape(x['summary'])
        article['text'] = text
        title = html.unescape(x['title'])
        article['title'] = title
        img = re.findall('<img src="([^"]*)"', x['content'][0]['value'])
        if img:
            article['img'] = img[0]
            article['img'] = re.sub('scale/geometry/([^/]*)/', 'scale/geometry/720/', article['img'])
        article['tags'] = get_tags(article['link'])
        data.append(article)
    return data[::-1]


def get_tags(link):
    sourcecode = requests.get(link).text
    tags = re.findall('name="keywords" content="([^"]*)"', sourcecode)
    tags = tags[0].split(',') if tags else tags
    return tags


def set_data(data, name):
    for article in data:
        n = news.News(name)
        n.set_img(article['img'] if 'img' in article else None)
        n.set_title(article['title'])
        n.set_text(article['text'])
        n.set_link(article['link'])
        n.set_tags(article['tags'])
        n.set_variante(2)
        n.post()


def check_site(name, alias, link, channel_id):
    db = database.Database()
    if not db.check_site(name):
        db.insert_site(name, alias, link)
        db.insert_channel(name, channel_id)


if __name__ == '__main__':
    main()
