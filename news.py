#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
import logging
import database
import telegrambot
from config import debug, owner
from hashids import Hashids
import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


class News:
    def __init__(self, site):
        self.__site = site
        self.__title = None
        self.__text = None
        self.__link = None
        self.__img = None
        self.__url = None
        self.__channel = None
        self.__date = None
        self.__tags = None
        self.__variante = 2
        self.__alias = None
        self.__id = None
        self.__hash = None

    def _get_data(self):
        return {'id': self.__id, 'alias': self.__alias, 'title': self.__title, 'text': self.__text, 'link': self.__link,
                'img': self.__img, 'url': self.__url, 'channel': self.__channel, 'date': self.__date,
                'tags': self.__tags, 'site': self.__site, 'hash': self.__hash}

    def __check(self, value):
        if value:
            value = value.replace('<br />', '')
            value = value.replace('<B>', '')
            value = value.replace('<B/>', '')
            value = value.replace('<p>', '')
            value = value.replace('</p>', '')
            value = value.replace('<p/>', '')
            value = value.replace('</strong>', '')
            value = value.replace('<strong>', '')
        return value

    def set_title(self, title):
        self.__title = self.__check(title)

    def __create_hashtag(self, text):
        text_list = re.split('[.:]', text, maxsplit=1)
        tags = re.split('[\/-]', text_list[0])
        tags = ['#' + tag.replace(' ', '') for tag in tags]
        new_text = ' '.join(tags) + text_list[1]
        for tag in tags:
            if len(tag) > 15:
                new_text = text
        return new_text

    def set_text(self, text, hashtag=False):
        if hashtag:
            text = self.__create_hashtag(text)
        self.__text = self.__check(text)

    def set_link(self, link):
        self.__link = self.__check(link)

    def set_img(self, img):
        self.__img = self.__check(img)

    def set_date(self, date):
        self.__date = date

    def set_variante(self, variante):
        self.__variante = variante

    def set_tags(self, tags):
        result = ''
        for tag in tags:
            tag = tag.replace('-', '').replace(' ', '').replace('.', '').replace('&', '').replace("'", '').replace('/',
                                                                                                                   '')
            result = result + ('#' if not tag[:1] == '#' else '') + tag + ' '
        self.__tags = result

    def _hash_id(self):
        hashids = Hashids(salt=config.salt, min_length=6)
        self.__hash = hashids.encode(self.__id)

    def __insert_db(self):
        db = database.Database()
        available = db.check_news(self.__link) if self.__link[:4] == 'http' else db.check_news(self.__url + self.__link)
        if not available:
            self.__id = db.insert_news(self.__title, self.__text, self.__link, self.__img, self.__site,
                                       date=self.__date,
                                       tags=self.__tags)
            self._hash_id()
            self.__url, self.__channel, self.__alias = db.get_data(self.__site)
            if debug:
                self.__channel = owner
            return True
        return False

    def __send_une(self):
        tg = telegrambot.telegram()
        tg.send_var1(self.__title, self.__text, self.__link, self.__hash, self.__img,
                     self.__channel, date=self.__date)

    def __send_deux(self):
        tg = telegrambot.telegram()
        tg.send_var2(self._get_data())

    def __send_trois(self):
        tg = telegrambot.telegram()
        tg.send_instant(self.__title, self.__link, self.__channel)

    def post(self):
        if self.__insert_db():
            if self.__variante == 1:
                self.__send_une()
            elif self.__variante == 2:
                self.__send_deux()
            elif self.__variante == 3:
                self.__send_trois()
