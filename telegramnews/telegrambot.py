#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import time
from _datetime import datetime
from pprint import pprint

from telegram.bot import Bot
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram.parsemode import ParseMode

from . import config

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


class Telegram:
    def __init__(self):
        self.__bot = Bot(config.bot_token)

    def __get_keyboard(self, link, hash):
        keyboard = [
            [
                InlineKeyboardButton("Artikel lesen ↗️", url=link),
                InlineKeyboardButton("Teilen 🗣", switch_inline_query=hash),
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

    def __get_keyboard_new(self, buttons):
        keyboard = []
        if "link" in buttons:
            keyboard.append(
                [InlineKeyboardButton("Artikel lesen ↗️", url=buttons["link"])]
            )
        return InlineKeyboardMarkup(keyboard)

    def send_var1(self, title, text, link, hash, img, channel_id, date=None):
        add = "_" + datetime.strftime(date, "%d.%m.%Y %H:%M") + "_\n" if date else ""
        msg = "*" + title + "*\n\n" + add + text[:-1] + "[.](" + img + ")"
        try:
            self.__bot.sendMessage(
                text=msg,
                chat_id=channel_id,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=self.__get_keyboard(link, hash),
            )
        except Exception as e:
            logging.exception(e)
        time.sleep(5)

    def send_var2(self, data, probably_msg_id):
        msg = "*{}*\n{}\n\n{}".format(data["title"], data["tags"], data["text"])
        arrow = "[👉](" + data["img"] + ")" if data["img"] else "👉"
        msg = "{}\n\n Teilen {} `t.me/{}/{}`".format(
            msg, arrow, data["site"], probably_msg_id
        )
        try:
            msg_id = self.__bot.sendMessage(
                text=msg,
                chat_id=data["channel"],
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=self.__get_keyboard(data["link"], data["hash"]),
            )["message_id"]
        except Exception as e:
            logging.exception(e)
            msg_id = False
        return msg_id

    def send_instant(self, title, link, channel_id):
        msg = "[" + title + "](" + link + ")"
        try:
            self.__bot.sendMessage(
                text=msg, chat_id=channel_id, parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            logging.exception(e)
        time.sleep(10)

    def send(self, msg, channel_id, keyboard):
        try:
            if config.debug == "text":
                pprint(msg+ str(keyboard))
                return 0
            msg_id = self.__bot.sendMessage(
                text=msg,
                chat_id=channel_id,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=self.__get_keyboard_new(keyboard),
            )["message_id"]
        except Exception as e:
            logging.exception(e)
            msg_id = 0
        return msg_id
