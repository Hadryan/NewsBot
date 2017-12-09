#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
import logging
import feedparser
import html
import news
import database

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def main():
    name = 'bild_de'
    alias = 'Bild.de'
    base_url = 'http://www.bild.de/'
    channel_id = -1001142790377

    check_site(name, alias, base_url, channel_id)

    data = get_data()
    set_data(data, name)


def get_data():
    raw_data = feedparser.parse('http://www.bild.de/rssfeeds/vw-news/vw-news-16726644,sort=1,view=rss2.bild.xml')
    data = []
    for x in raw_data['entries']:
        article = dict()
        article['link'] = x['link']
        text = x['summary']
        text = re.split('\n', text, re.MULTILINE)
        article['text'] = html.unescape(text[-1].split('<br />')[0])
        title = html.unescape(x['title'])
        article['title'] = title
        img = x['media_thumbnail'][0]['url'].replace(',w=120,', ',w=1200,') if 'media_thumbnail' in x else None
        article['img'] = img
        tags = x['tags']
        tags = [y['term'] for y in tags]
        article['tags'] = tags
        data.append(article)
    return data[::-1]


def set_data(data, name):
    for article in data:
        n = news.News(name)
        n.set_img(article['img'])
        n.set_title(article['title'])
        n.set_text(article['text'])
        n.set_link(article['link'])
        n.set_tags(article['tags'])
        n.post()


def check_site(name, alias, link, channel_id):
    db = database.Database()
    if not db.check_site(name):
        db.insert_site(name, alias, link)
        db.insert_channel(name, channel_id)


if __name__ == '__main__':
    main()
