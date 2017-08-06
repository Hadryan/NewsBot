#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
import news


def main():
    base_url = 'http://www.brohltal-info24.de/'
    response = requests.get(base_url + 'index.php?site=news-direkt').text
    data = re.findall('img src="([^"]*)".*\r\n.*\r\n.*\r\n[ ]*(.*?)[ ]*<.*?<br>[ \r\n]*(.*) <a href=([^>]*)', response)


def set_data(data):
    for article in data:
        n = news.News()
        n.set_img(article[0])
        n.set_title(article[1])
        n.set_text(article[2])
        n.set_link(article[3])

if __name__ == '__main__':
    main()
