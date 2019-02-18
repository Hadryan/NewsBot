#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import re
from datetime import datetime

import pytz
from hashids import Hashids

import config
import database
import telegrambot
from variants import VERSION_1, VERSION_2, VERSION_3

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

TIMEZONE = "Europe/Berlin"


class Article:
    def __init__(
        self, site, short="", title="", text="", link="", img="", date="", tags=""
    ):
        self.__site = site
        self.__short = short
        self.__title = title
        self.__text = text
        self.__link = link
        self.__img = img
        self.__date = date
        self.__tags = tags
        self.__variant = 0
        self.__share_link = 0
        self.__id = 0
        self.__sent = False

    @property
    def title(self):
        if not self.__title:
            return ""
        return self.__title + "\n"

    @title.setter
    def title(self, title):
        self.__title = self.__check(title)

    @property
    def text(self):
        if not self.__text:
            return ""
        if self.__img and not self.__share_link:
            if "." in self.__text:
                dot = self.__text.rindex(".")
            else:
                dot = len(self.__text)
            return (
                "{}[.]({}){}".format(
                    self.__text[:dot], self.__img, self.__text[dot + 1 :]
                )
                + "\n\n"
            )
        return self.__text + "\n\n"

    @text.setter
    def text(self, text):
        self.__text = self.__check(text)

    @property
    def link(self):
        return self.__link

    @link.setter
    def link(self, link):
        self.__link = self.__check(link)

    @property
    def img(self):
        return self.__img

    @img.setter
    def img(self, img):
        self.__img = self.__check(img)

    @property
    def date(self):
        return (
            pytz.utc.localize(datetime.strptime(self.__date, "%Y-%m-%d %H:%M:%S"))
            .astimezone(pytz.timezone(TIMEZONE))
            .strftime("Artikel vom %d.%m.%Y um %H:%M Uhr")
            + "\n"
        )

    @date.setter
    def date(self, date):
        self.__date = self.__check(date)

    @property
    def tags(self):
        if self.__tags:
            if self.__variant == 3:
                return "\n#{}".format(" #".join(self.__tags))
            return "#{}\n\n".format(" #".join(self.__tags))
        return "\n"

    @tags.setter
    def tags(self, tags):
        self.__tags = self.__clean_tags(tags)

    def __check(self, value):
        purge = [
            "<br />",
            "<B>",
            "<B/>",
            "<p>",
            "</p>",
            "<p/>",
            "</strong>",
            "<strong>",
        ]
        if value:
            for expr in purge:
                value = value.replace(expr, "")
        return value

    def __clean_tags(self, tags):
        purge = ["-", " ", ".", "&", "'", "/", "@", "#"]
        for char in purge:
            tags = [tag.replace(char, "") for tag in tags]
        return tags

    @property
    def share_link(self):
        db = database.Database()
        probably_msg_id = db.get_max_message_id(self.__site)
        probably_msg_id = int(probably_msg_id if probably_msg_id else 0) + 1
        arrow = "[👉]({})".format(self.__img) if self.__img else "👉"
        share = "Teilen {}".format(arrow)
        if self.__share_link == 1:
            return "{}`t.me/{}/{}`".format(share, self.__site, probably_msg_id)
        elif self.__share_link == 2:
            return "{} `@DerNewsBot {}{}`".format(share, self.__short, probably_msg_id)
        elif self.__share_link == 3 and self.__id:
            hashids = Hashids(salt=config.salt, min_length=6)
            hash = hashids.encode(self.__id)
            return "{} `@DerNewsBot {}`".format(share, hash)
        return ""

    def __insert_db(self, db):
        exists = db.check_news(self.__link) or db.check_news(
            re.findall(r"https?://[\-\w.]*/(.*)$", self.__link)[0]
        )
        if not exists:
            self.__id = db.insert_news(
                self.__title,
                self.__text,
                self.__link,
                self.__img,
                self.__site,
                date=self.__date,
                tags=self.tags,
            )
            return True
        return False

    def create(self, variant=0, share_link=0):
        self.__variant = variant
        self.__share_link = share_link
        if variant in [0, 3]:
            return (
                VERSION_1.format(
                    title=self.title,
                    text=self.text,
                    tags=self.tags,
                    share=self.share_link,
                ),
                {"link": self.link},
            )
        elif variant == 1:
            return (VERSION_2.format(title=self.title, link=self.link), {})
        elif variant == 2:
            return VERSION_3.format(title=self.title, text=self.text, date=self.date)

    def send(self, db, channel_id, variant, share_link=2):
        if not self.__insert_db(db):
            return
        tg = telegrambot.Telegram()
        text, buttons = self.create(variant=variant, share_link=share_link)
        msg_id = tg.send(
            text, channel_id if not config.debug else config.owner, buttons
        )
        if msg_id:
            db.update_message_id(self.__id, msg_id)
