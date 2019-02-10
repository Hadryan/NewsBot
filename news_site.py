import database
import news


class Site:
    def __init__(self):
        self.__name = ""
        self.__alias = ""
        self.__base_url = ""
        self.__channel_id = 0
        self.__db = database.Database()
        self.__articles = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def alias(self):
        return self.__alias

    @alias.setter
    def alias(self, alias):
        self.__alias = alias

    @property
    def base_url(self):
        return self.__base_url

    @base_url.setter
    def base_url(self, base_url):
        self.__base_url = base_url

    @property
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, channel_id):
        self.__channel_id = channel_id

    def check_site(self):
        if self.__db.check_site(self.__name):
            self.__db.update_site(self.__name, self.__alias, self.__base_url)
        else:
            self.__db.insert_site(self.__name, self.__alias, self.__base_url)
            self.__db.insert_channel(self.__name, self.__channel_id)

    def add_article(self, title="", text="", img="", link="", tags: list = None, date=""):
        n = news.News(self.__name)
        if title:
            n.set_title(title)
        if text:
            n.set_text(text)
        if img:
            n.set_img(img)
        if link:
            n.set_link(link)
        if tags:
            n.set_tags(tags)
        if date:
            n.set_date(date)
        self.__articles.append(n)

    def post(self, variant=2):
        self.check_site()
        for article in self.__articles[::-1]:
            article.set_variante(variant)
            article.post()
