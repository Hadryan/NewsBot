#!/usr/bin/env python
# -*- coding: utf-8 -*-


import database
import telegrambot


class News:
    def __init__(self, site):
        self.__site = site
        self.__title = None
        self.__text = None
        self.__link = None
        self.__img = None
        self.__url = None
        self.__channel = None

    def __check(self, value):
        value = value.replace('</br>', '')
        if value == '':
            raise ValueError
        return value

    def set_title(self, title):
        self.__title = self.__check(title)

    def set_text(self, text):
        self.__text = self.__check(text)

    def set_link(self, link):
        self.__link = self.__check(link)

    def set_img(self, img):
        self.__img = self.__check(img)

    def __insert_db(self):
        db = database.Database()
        if not db.check_news(self.__title):
            db.insert_news(self.__title, self.__text, self.__link, self.__img, self.__site)
        self.__url, self.__channel  = db.get_data(self.__site)

    def __send(self):
        tg = telegrambot.telegram()
        tg.send_news(self.__title, self.__text, self.__url + self.__link, self.__url + self.__img, self.__channel)

    def post(self):
        self.__insert_db()
        self.__send()
