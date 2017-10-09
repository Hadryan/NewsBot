#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
import logging
import feedparser
import html
import requests
import time
import news
import database

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def main():
    name = 'golem'
    base_url = 'https://golem.de/'
    channel_id = -1001138540100

    check_site(name, base_url, channel_id)

    data = get_data()
    set_data(data, name)


# This function determines the original image because the image in the feed has a bad resolution
def get_img(img):
    result = 404
    value = 0
    img = re.findall('<img src="([^"]*)"', img)[0]
    img = img.rsplit('/', maxsplit=1)
    while not result == 200 and not value > 10:
        numbers = img[1].split('-')
        value = (value + 1) * - 1 if value >= 0 else value * - 1
        numbers = numbers[0] + '-' + str(int(numbers[1]) + value) + '-' + numbers[2]
        result = requests.get(img[0] + '/sp_' + numbers).status_code
        time.sleep(0.5)
    img = img[0] + '/sp_' + numbers
    return img


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
        article['img'] = get_img(x['content'][0]['value'])
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


def check_site(name, link, channel_id):
    db = database.Database()
    if not db.check_site(name):
        db.insert_site(name, link)
        db.insert_channel(name, channel_id)


if __name__ == '__main__':
    main()
