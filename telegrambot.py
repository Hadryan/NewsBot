#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
import config
from _datetime import datetime


class telegram():
    def __init__(self):
        self.__bot = Bot(config.bot_token)

    def send_news(self, title, text, link, img, channel_id, date=None):
        add = '_' + datetime.strftime(date, "%d.%m.%Y %H:%M") + '_\n' if date else ''
        msg = '*' + title + '*\n\n' + add + text[:-1] + '[.](' + img + ')'
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('Artikel lesen', url=link)]])
        self.__bot.sendMessage(text=msg, chat_id=channel_id, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)
        time.sleep(5)
