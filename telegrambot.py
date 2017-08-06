#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
import config


class telegram():
    def __init__(self):
        self.__bot = Bot(config.bot_token)

    def send_news(self, title, text, link, img, channel_id):
        msg = '*' + title + '*\n\n' + text[:-1] + '[.](' + img + ')'
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('Artikel anzeigen', url=link)]])
        self.__bot.sendMessage(text=msg, chat_id=channel_id, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)
        time.sleep(10)
