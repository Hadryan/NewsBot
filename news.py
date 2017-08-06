#!/usr/bin/env python
# -*- coding: utf-8 -*-


import database


class News:
    def __init__(self, site):
        self.__site = site
        self.__title = None
        self.__text = None
        self.__link = None
        self.__img = None

    def __check(self, value):
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

    def post(self):
        db = database.Database()
        db.insert_news(self.__title, self.__text, self.__link, self.__img, self.__site)
