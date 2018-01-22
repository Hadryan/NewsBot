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
    name = 'golem_de'
    alias = 'Golem.de'
    base_url = 'https://golem.de/'
    channel_id = -1001138540100

    check_site(name, alias, base_url, channel_id)

    data = get_data()
    set_data(data, name)


def get_data():
    raw_data = feedparser.parse('https://rss.golem.de/rss.php?feed=RSS2.0')
    data = []
    for x in raw_data['entries']:
        article = dict()
        article['link'] = x['link']
        text = html.unescape(x['summary'].split('(<a')[0])
        article['text'] = text
        title = html.unescape(x['title'])
        article['title'] = title
        article_code = requests.get(article['link']).text
        article['img'] = re.findall('"twitter:image" property="og:image" content="([^"]*)"', article_code)[0]
        tags = re.findall('a href="[^"]*">([^<]*)<', html.unescape(x['summary']))
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
    if db.check_site(name):
        db.update_site(name, alias, link)
    else:
        db.insert_site(name, alias, link)
        db.insert_channel(name, channel_id)


if __name__ == '__main__':
    main()
