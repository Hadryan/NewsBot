#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
import news
import database


def main():
    name = 'brohltal'
    base_url = 'http://www.brohltal-info24.de/'
    channel_id = 1131410143

    check_site(name, base_url, channel_id)

    data = get_data(base_url)
    set_data(data, name, base_url)


def get_data(base_url):
    data_list = []
    url = base_url + 'index.php?site='
    sites = ['news-direkt', 'newsaw-direkt', 'newsregio-direkt']
    for site in sites:
        response = requests.get(url + site).text
        data = re.findall('img src="([^"]*)".*\r\n.*\r\n.*\r\n[ ]*(.*?)[ ]*<.*?<br>[ \r\n]*(.*) <a href=([^>]*)',
                          response)[::-1]
        data_list = data_list + data
    return data_list


def set_data(data, name, base_url):
    for article in data:
        n = news.News(name)
        n.set_img(article[0])
        n.set_title(article[1])
        n.set_text(article[2])
        n.set_link(article[3])
        n.post()


def check_site(name, link, channel_id):
    db = database.Database()
    if not db.check_site(name):
        db.insert_site(name, link)
        db.insert_channel(name, channel_id)


if __name__ == '__main__':
    main()
