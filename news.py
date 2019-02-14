#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import re

from hashids import Hashids

import config
import database
import telegrambot
from config import debug, owner

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


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
        self.__share_link = 0
        self.__alias = None
        self.__short = None
        self.__id = None
        self.__hash = None

    def _get_data(self):
        return {
            "id": self.__id,
            "alias": self.__alias,
            "title": self.__title,
            "text": self.__text + self.get_share_link(),
            "link": self.__link,
            "img": self.__img,
            "url": self.__url,
            "channel": self.__channel,
            "date": self.__date,
            "tags": self.__tags,
            "site": self.__site,
            "hash": self.__hash,
        }

    def __check(self, value):
        if value:
            value = value.replace("<br />", "")
            value = value.replace("<B>", "")
            value = value.replace("<B/>", "")
            value = value.replace("<p>", "")
            value = value.replace("</p>", "")
            value = value.replace("<p/>", "")
            value = value.replace("</strong>", "")
            value = value.replace("<strong>", "")
        return value

    def set_title(self, title):
        self.__title = self.__check(title)

    def set_text(self, text):
        self.__text = self.__check(text)

    def set_link(self, link):
        self.__link = self.__check(link)

    def set_img(self, img):
        self.__img = self.__check(img)

    def set_date(self, date):
        self.__date = date

    def set_variante(self, variante):
        self.__variante = variante

    def get_share_link(self):
        db = database.Database()
        probably_msg_id = db.get_max_message_id(self.__site)
        probably_msg_id = int(probably_msg_id if probably_msg_id else 0) + 1
        arrow = "[👉](" + self.__img + ")" if self.__img else "👉"
        share = "\n\n Teilen {}".format(arrow)
        if self.share_link == 1:
            return "{}`t.me/{}/{}`".format(share, self.__site, probably_msg_id)
        elif self.share_link == 2:
            return "{} `@DerNewsBot {}{}`".format(share, self.__short, probably_msg_id)
        return ""

    @property
    def share_link(self):
        return self.__share_link

    @share_link.setter
    def share_link(self, share_link):
        self.__share_link = share_link

    def set_tags(self, tags):
        result = ""
        for tag in tags:
            tag = (
                tag.replace("-", "")
                .replace(" ", "")
                .replace(".", "")
                .replace("&", "")
                .replace("'", "")
                .replace("/", "")
            )
            result = result + ("#" if not tag[:1] == "#" else "") + tag + " "
        self.__tags = result

    def _hash_id(self):
        hashids = Hashids(salt=config.salt, min_length=6)
        self.__hash = hashids.encode(self.__id)

    def __insert_db(self):
        db = database.Database()
        available = db.check_news(self.__link) or db.check_news(
            re.findall(r"https?://[\-\w.]*/(.*)$", self.__link)[0]
        )
        if not available:
            self.__id = db.insert_news(
                self.__title,
                self.__text,
                self.__link,
                self.__img,
                self.__site,
                date=self.__date,
                tags=self.__tags,
            )
            self._hash_id()
            self.__url, self.__channel, self.__alias, self.__short = db.get_data(
                self.__site
            )
            if debug:
                self.__channel = owner
            return True
        return False

    def __send_une(self):
        tg = telegrambot.Telegram()
        tg.send_var1(
            self.__title,
            self.__text,
            self.__link,
            self.__hash,
            self.__img,
            self.__channel,
            date=self.__date,
        )

    def __send_deux(self):
        db = database.Database()
        tg = telegrambot.Telegram()
        probably_msg_id = db.get_max_message_id(self.__site)
        probably_msg_id = int(probably_msg_id if probably_msg_id else 0) + 1
        self.__msg_id = tg.send_var2(self._get_data(), probably_msg_id)
        if self.__msg_id:
            db.update_message_id(self.__id, self.__msg_id)

    def __send_trois(self):
        tg = telegrambot.Telegram()
        tg.send_instant(self.__title, self.__link, self.__channel)

    def post(self):
        if self.__insert_db():
            if self.__variante == 1:
                self.__send_une()
            elif self.__variante == 2:
                self.__send_deux()
            elif self.__variante == 3:
                self.__send_trois()
