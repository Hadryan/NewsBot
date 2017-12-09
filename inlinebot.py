#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uuid import uuid4
from hashids import Hashids
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, InlineKeyboardMarkup, \
    InlineKeyboardButton
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import logging
import config
import database

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text('Hi!')


def help(bot, update):
    update.message.reply_text('Help!')


def inlinequery(bot, update):
    """Handle the inline query."""
    query = update.inline_query.query
    my_id = uuid4()
    hashids = Hashids(salt=config.salt, min_length=6)
    news_id = hashids.decode(query)[0]
    db = database.Database()
    title, text, link, img_link, tags, added, alias, name = db.get_news(news_id)
    results = [
        InlineQueryResultArticle(
            id=my_id,
            title=title,
            description=text,
            thumb_url=img_link,
            input_message_content=InputTextMessageContent(
                message_text="*{}*\n\n{}\n[Foto]({})".format(title, text, img_link),
                parse_mode=ParseMode.MARKDOWN),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    text='Artikel lesen ↗️',
                    url=link),
                InlineKeyboardButton(
                    text='Mehr {}'.format(alias),
                    url="https://t.me/" + name
                )]]
            )
        )
    ]

    update.inline_query.answer(results)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater(config.bot_token)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(InlineQueryHandler(inlinequery))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
