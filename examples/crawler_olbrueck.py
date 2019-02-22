#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

import logging
import os
from datetime import datetime, timedelta
from urllib.request import urlretrieve

import requests

from telegramnews import Site

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def create_jpg(file_name):
    cmd = 'convert -limit memory 500000000 -limit map 500000000 -resize 50% -density 200 -quality 50 "{0}"pdf[0] \
    -bordercolor white -border 0x0 -trim -alpha remove "{0}"jpg'
    os.system(cmd.format(file_name[:-3]))
    return file_name[:-3] + "jpg"


def get_newspaper(site, week=0):
    week = datetime.now() + timedelta(weeks=week)
    base_url = "https://archiv.wittich.de/epapers/pdf/3/{}/{}.pdf"
    url = base_url.format(week.year, week.isocalendar()[1])
    if site.check_article_exists(url):
        return []
    pdf = os.path.join(
        os.path.dirname(__file__),
        "downloads/olbrueck_{}-{}.pdf".format(week.year, week.isocalendar()[1]),
    )
    response = requests.head(url)
    if "status" in response.headers and response.headers["status"] == "404 Not found":
        return []
    urlretrieve(url, pdf)
    jpg = create_jpg(pdf)
    title = "Olbrück Rundschau Nr. {}".format(week.isocalendar()[1])
    return [title, jpg, url]


def main():
    site = Site()
    site.name = "obrueck"
    site.alias = "Olbrück Rundschau"
    site.base_url = "https://archiv.wittich.de/epapers/pdf/3"
    site.short = "olbrück"
    site.channel_id = -1001199332289

    for i in range(10):
        result = get_newspaper(site, week=(i - 5) * -1)
        if result:
            title, jpg, url = tuple(result)
            site.add_article(title=title, img=jpg, link=url)
    site.post(4)


if __name__ == "__main__":
    main()
