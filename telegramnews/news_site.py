import re

from telegramnews.database import Database
from . import database, news


class Site:
    def __init__(self, name="", alias="", short="", base_url="", channel_id=0):
        self.__name = name
        self.__alias = alias
        self.__short = short
        self.__base_url = base_url
        self.__channel_id = channel_id
        self.__instant_id = 0
        self.__join_instant = ""
        self.__instant_hash = ""
        self.__db = database.Database()
        self.__articles = []
        self.check_site()
        self.__sent = False

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name
        self.check_site()

    @property
    def alias(self):
        return self.__alias

    @alias.setter
    def alias(self, alias):
        self.__alias = alias
        self.check_site()

    @property
    def short(self):
        return self.__short

    @short.setter
    def short(self, short):
        self.__short = short
        self.check_site()

    @property
    def base_url(self):
        return self.__base_url

    @base_url.setter
    def base_url(self, base_url):
        self.__base_url = base_url
        self.check_site()

    @property
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, channel_id):
        self.__channel_id = channel_id
        self.check_site()

    @property
    def instant_id(self):
        return self.__instant_id

    @instant_id.setter
    def instant_id(self, instant_id):
        self.__instant_id = instant_id
        self.check_site()

    @property
    def join_instant(self):
        return self.__join_instant

    @join_instant.setter
    def join_instant(self, join_instant):
        self.__join_instant = join_instant
        self.check_site()

    @property
    def instant_hash(self):
        return self.__instant_hash

    @instant_hash.setter
    def instant_hash(self, instant_hash):
        self.__instant_hash = instant_hash
        self.check_site()

    def check_article_exists(self, link):
        db = Database()
        return db.check_news(link) or db.check_news(
            re.findall(r"https?://[\-\w.]*/(.*)$", link)[0]
        )

    def check_site(self):
        if not (self.__short or self.__alias or self.__base_url or self.__name):
            return
        if self.__db.check_site(self.__name):
            self.__db.update_site(
                self.__name, self.__alias, self.__short, self.__base_url
            )
        else:
            if not (self.__channel_id):
                return
            self.__db.insert_site(
                self.__name, self.__alias, self.__short, self.__base_url
            )
            self.__db.insert_channel(self.__name, self.__channel_id)

    def add_article(
        self, title="", text="", img="", link="", tags: list = None, date=""
    ):
        n = news.Article(self.name, short=self.short, alias=self.alias)
        if title:
            n.title = title
        if text:
            n.text = text
        if img:
            n.img = img
        if link:
            n.link = link
        if tags:
            n.tags = tags
        if date:
            n.date = date
        self.__articles.append(n)

    def post(self, variant=0, share_link=2):
        for article in self.__articles[::-1]:
            article.send(
                self.__db,
                self.channel_id,
                variant,
                share_link=share_link,
                instant=[self.instant_id, self.join_instant, self.instant_hash],
            )
