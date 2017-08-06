#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
import logging
import database
import telegrambot

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

    def __check(self, value):
        value = value.replace('<br />', '')
        value = value.replace('<B>', '')
        value = value.replace('<B/>', '')
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

    def set_tags(self, tags):
        result = ''
        for tag in tags:
            tag = tag.replace('-', '').replace(' ', '').replace('.', '')
            result = result + ('#' if not tag[:1] == '#' else '') + tag + ' '
        self.__tags = result

    def __insert_db(self):
        db = database.Database()
        if not db.check_news(self.__link):
            db.insert_news(self.__title, self.__text, self.__link, self.__img, self.__site, date=self.__date,
                           tags=self.__tags)
            self.__url, self.__channel = db.get_data(self.__site)
            return True
        return False

    def __send_une(self):
        tg = telegrambot.telegram()
        tg.send_var1(self.__title, self.__text, self.__url + self.__link, self.__url + self.__img, self.__channel,
                     date=self.__date)

    def __send_deux(self):
        tg = telegrambot.telegram()
        tg.send_var2(self.__title, self.__text, self.__link, self.__img, self.__tags, self.__channel)

    def post(self):
        if self.__insert_db():
            self.__send_deux()
