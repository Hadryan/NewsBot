#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
from _datetime import datetime
from urllib.request import urlopen

import database
from news_site import Site

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def main():
    site = Site()
    site.name = 'brohltal'
    site.alias = 'BrohltalInfo24'
    site.base_url = 'http://www.brohltal-info24.de/'
    site.channel_id = -1001131410143

    for article in get_data(site.base_url):
        text, tags = create_hashtag(article[2])
        site.add_article(img=site.base_url + article[0], title=article[1], text=text, tags=tags, date=article[4],
                         link=site.base_url + article[3])
    site.post(variant=1)


def create_hashtag(text):
    text_list = re.split('[.:]', text, maxsplit=1)
    tags = re.split('[\/-]', text_list[0])
    tags = ['#' + tag.replace(' ', '') for tag in tags]
    new_text = text_list[1]
    for tag in tags:
        if len(tag) > 15:
            return text, []
    return new_text, tags


def read_data(url, site, limit=None):
    add = '&limit=' + str(limit) if limit else ''
    response = urlopen(url + site + add).read().decode('cp1252').replace('–', '-')
    data = re.findall('img src="([^"]*)".*\r\n.*\r\n.*\r\n[ ]*(.*?)[ ]*<.*?<br>[ \r\n]*(.*) <a href=([^>]*)>.*\r\n'
                      + '[ ]*([0-9\.]* [0-9\:]*)', response)[::-1]
    return list(data)


def read_all_data(url, site):
    limit = 0
    result = 1
    data = []
    while result > 0:
        adata = read_data(url, site, limit=limit)
        data = data + adata
        result = len(adata)
        limit = limit + 30
    return data


def get_data(base_url):
    data_list = []
    url = base_url + 'index.php?site='
    sites = ['newsregio-direkt', 'newsaw-direkt', 'news-direkt']
    for site in sites:
        data_list = data_list + read_data(url, site)
    data_list = [list(item) for item in data_list]
    for item in data_list:
        item[4] = datetime.strptime(item[4], '%d.%m.%y %H:%M')
    data_list.sort(key=lambda r: r[4])
    for x in data_list:
        x[4] = None
    return data_list


if __name__ == '__main__':
    main()
