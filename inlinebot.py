#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
from uuid import uuid4

from hashids import Hashids
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
    ParseMode,
)
from telegram.ext import CommandHandler, InlineQueryHandler, Updater

import config
import database

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text("Hi!")


def help(bot, update):
    update.message.reply_text("Help!")


def create_article(title, text, link, img_link, tags, added, alias, name):
    return InlineQueryResultArticle(
        id=uuid4(),
        title=title,
        description=text,
        thumb_url=img_link,
        input_message_content=InputTextMessageContent(
            message_text="*{}*\n_Artikel vom {} Uhr_\n\n{}\n[Foto]({})".format(
                title,
                "{2}.{1}.{0} {3}:{4}".format(*re.split(r"[- :]", added)),
                text,
                img_link,
            ),
            parse_mode=ParseMode.MARKDOWN,
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Artikel lesen ↗️", url=link),
                    InlineKeyboardButton(
                        text="Mehr {}".format(alias), url="https://t.me/" + name
                    ),
                ]
            ]
        ),
    )


def inlinequery(bot, update):
    """Handle the inline query."""
    query = update.inline_query.query
    db = database.Database()
    results = []
    if re.findall("^([a-zA-Z]+)$", query):
        short = re.findall("^([a-zA-Z]+)$", query)
        news = db.get_last_news(short[0])
        for new in news:
            results.append(create_article(*new))
    elif re.findall("^([a-zA-Z]+[0-9]+)$", query):
        article = db.get_news_by_id(*re.findall("^([a-zA-Z]+)([0-9]+)$", query)[0])
        if article:
            results.append(create_article(*article))
    else:
        hashids = Hashids(salt=config.salt, min_length=6)
        news_id = hashids.decode(query)[0]
        results.append(create_article(*db.get_news(news_id)))
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


if __name__ == "__main__":
    main()
