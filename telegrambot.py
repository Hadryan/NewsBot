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
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('Artikel lesen ↗️', url=link)]])
        try:
            self.__bot.sendMessage(text=msg, chat_id=channel_id, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)
        except Exception as e:
            logging.exception(e)
        time.sleep(5)

    def send_var2(self, data):
        msg = '*' + data['title'] + '*\n' + data['tags'] + '\n\n' + data['text']
        msg = msg + '\n[Foto](' + data['img'] + ')' if data['img'] else msg
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('Artikel lesen ↗️', url=data['link']),
                                          InlineKeyboardButton('Teilen 🗣', switch_inline_query=data['hash'])]])
        try:
            self.__bot.sendMessage(text=msg, chat_id=data['channel'], parse_mode=ParseMode.MARKDOWN,
                                   reply_markup=keyboard)
        except Exception as e:
            logging.exception(e)
        time.sleep(10)

    def send_instant(self, title, link, channel_id):
        msg = '[' + title + '](' + link + ')'
        try:
            self.__bot.sendMessage(text=msg, chat_id=channel_id, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            logging.exception(e)
        time.sleep(10)
