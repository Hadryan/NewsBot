#!/usr/bin/env python
# -*- coding: utf-8 -*-
import html
import logging
import re

import requests

import database
import news

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def main():
    name = "cashys"
    base_url = "http://stadt-bremerhaven.de/"
    channel_id = -100

    check_site(name, base_url, channel_id)

    data = get_data(base_url)
    set_data(data, name)


def read_data(url):
    print(url)
    response = requests.get(url).text
    data = re.findall(
        '<h3><a href="([^"]*)">([^<]*).*?Kategorie(.*?)</span>.*?data-recalc-dims="1"/>(.*?)</p></div>',
        response,
        re.MULTILINE | re.DOTALL,
    )[::-1]
    return list(data)


def get_img(url):
    code = requests.get(url).text


def get_data(base_url):
    data_list = read_data(base_url)
    data = []
    for x in data_list:
        article = dict()
        text = html.unescape(x[3]).replace("</strong>", "*").replace("<strong>", "*")
        text = re.sub(r'<a href="[^"]*".*?>([^<]*)</a>', r"\1", text)
        text = re.sub("<.?span[^>]*>", "", text)
        article["text"] = text
        article["title"] = html.unescape(x[1])
        article["link"] = x[0]
        tags = x[2].split("geschrieben von")[0]
        tags = re.findall('tag">([^<]*)', tags)
        article["tags"] = tags
        article["img"] = get_img(x[0])
        data.append(article)
    return data


def set_data(data, name):
    for article in data:
        n = news.News(name)
        n.set_img(article["img"])
        n.set_title(article["title"])
        n.set_text(article["text"])
        n.set_link(article["link"])
        n.set_tags(article["tags"])
        n.post()


def check_site(name, link, channel_id):
    db = database.Database()
    if not db.check_site(name):
        db.sert_site(name, link)
        db.insert_channel(name, channel_id)


if __name__ == "__main__":
    main()
