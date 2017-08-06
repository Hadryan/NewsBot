#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from urllib.request import urlopen
from _datetime import datetime
import logging
import news
import database

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def main():
    name = 'brohltal'
    base_url = 'http://www.brohltal-info24.de/'
    channel_id = -1001131410143

    check_site(name, base_url, channel_id)

    data = get_data(base_url)
    set_data(data, name)


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
    return data_list


def set_data(data, name):
    for article in data:
        n = news.News(name)
        n.set_img(article[0])
        n.set_title(article[1])
        n.set_text(article[2], hashtag=True)
        n.set_link(article[3])
        n.set_date(article[4])
        n.set_variante(1)
        n.post()


def check_site(name, link, channel_id):
    db = database.Database()
    if not db.check_site(name):
        db.insert_site(name, link)
        db.insert_channel(name, channel_id)


if __name__ == '__main__':
    main()
