#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
import news
import database


def main():
    name = 'brohltal'
    base_url = 'http://www.brohltal-info24.de/'
    check_site(name, base_url)
    response = requests.get(base_url + 'index.php?site=news-direkt').text
    data = re.findall('img src="([^"]*)".*\r\n.*\r\n.*\r\n[ ]*(.*?)[ ]*<.*?<br>[ \r\n]*(.*) <a href=([^>]*)', response)
    set_data(data)


def set_data(data):
    for article in data:
        n = news.News('brohltal')
        n.set_img(article[0])
        n.set_title(article[1])
        n.set_text(article[2])
        n.set_link(article[3])
        n.post()

def check_site(name, link):
    db = database.Database()
    if not db.check_site(name):
        db.insert_site(name, link)


if __name__ == '__main__':
    main()
