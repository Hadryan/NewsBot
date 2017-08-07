#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
import logging
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
import config
from _datetime import datetime


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


class telegram():
    def __init__(self):
        self.__bot = Bot(config.bot_token)

    def send_var1(self, title, text, link, img, channel_id, date=None):
        add = '_' + datetime.strftime(date, "%d.%m.%Y %H:%M") + '_\n' if date else ''
        msg = '*' + title + '*\n\n' + add + text[:-1] + '[.](' + img + ')'
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('Artikel lesen', url=link)]])
        try:
            self.__bot.sendMessage(text=msg, chat_id=channel_id, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)
        except Exception as e:
            logging.exception(e)
        time.sleep(5)

    def send_var2(self, title, text, link, tags, channel_id, img=None):
        msg = '*' + title + '*\n' + tags + '\n\n' + text
        msg = msg + '\n[Foto](' + img + ')' if img else msg
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('Artikel lesen', url=link)]])
        try:
            self.__bot.sendMessage(text=msg, chat_id=channel_id, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)
        except Exception as e:
            logging.exception(e)
        time.sleep(10)