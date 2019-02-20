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

    def __get_keyboard(self, buttons):
        keyboard = []
        if "link" in buttons:
            keyboard.append(
                [InlineKeyboardButton("Artikel lesen ↗️", url=buttons["link"])]
            )
        if "magazine" in buttons:
            keyboard.append(
                [InlineKeyboardButton("Ausgabe lesen ↗️", url=buttons["magazine"])]
            )
        return InlineKeyboardMarkup(keyboard)

    def send_img(self, msg, channel_id, keyboard, img):
        try:

            msg_id = self.__bot.send_photo(
                caption=msg,
                photo=img if img[:4] == "http" else open(img, "rb"),
                chat_id=channel_id,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=self.__get_keyboard(keyboard),
            )
        except Exception as e:
            logging.exception(e)
            msg_id = 0
        return msg_id

    def send(self, msg, channel_id, buttons):
        if config.debug == "text":
            pprint(msg + str(buttons))
            return 0
        try:
            msg_id = self.__bot.sendMessage(
                text=msg,
                chat_id=channel_id,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=self.__get_keyboard(buttons),
            )["message_id"]
        except Exception as e:
            logging.exception(e)
            msg_id = 0
        return msg_id
