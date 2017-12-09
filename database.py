#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os


class Database():
    def __init__(self):
        file = os.path.join(os.path.dirname(__file__), 'data.db')
        self.__check_db(file)
        self.con = sqlite3.connect(file)
        self.cur = self.con.cursor()

    def check_site(self, name):
        self.cur.execute("SELECT id FROM sites WHERE name=?", (name,))
        if len(self.cur.fetchall()) < 1:
            return False
        return True

    def insert_site(self, name, alias, link):
        self.cur.execute("INSERT INTO sites (name, alias, link) VALUES(?, ?, ?)", (name, alias, link))
        self.con.commit()

    def check_news(self, link):
        self.cur.execute("SELECT id FROM news WHERE link=?", (link,))
        if len(self.cur.fetchall()) < 1:
            return False
        return True

    def insert_news(self, title, text, link, img, site, date=None, tags=None):
        img = '' if not img else img
        if date:
            self.cur.execute("INSERT INTO news (title, text, link, img_link, added, site_id) VALUES(?, ?, ?, ?, ?, "
                             + "(SELECT id FROM sites WHERE name=?))", (title, text, link, img, date, site))
        elif tags:
            self.cur.execute("INSERT INTO news (title, text, link, img_link, tags, site_id) VALUES(?, ?, ?, ?, ?, "
                             + "(SELECT id FROM sites WHERE name=?))", (title, text, link, img, tags, site))
        else:
            self.cur.execute("INSERT INTO news (title, text, link, img_link, site_id) VALUES(?, ?, ?, ?, "
                             + "(SELECT id FROM sites WHERE name=?))", (title, text, link, img, site))
        self.con.commit()
        self.cur.execute("SELECT MAX(id) FROM news")
        return self.cur.fetchall()[0][0]

    def insert_channel(self, site, channel_id):
        self.cur.execute("INSERT INTO channels (site_id, channel_id) VALUES ("
                         + "(SELECT id FROM sites WHERE name=?), ?)", (site, channel_id))
        self.con.commit()

    def get_data(self, site_name):
        self.cur.execute("SELECT s.link, c.channel_id, s.alias FROM sites s INNER JOIN channels c ON s.id=c.site_id WHERE "
                         + "s.name=?", (site_name,))
        return self.cur.fetchall()[:][0]

    def get_news(self, news_id):
        self.cur.execute("SELECT n.title, n.text, n.link, n.img_link, n.tags, n.added, s.alias FROM news n INNER JOIN "
                         + "sites s ON n.site_id=s.id INNER JOIN channels c on s.id=c.site_id WHERE n.id=?", (news_id,))
        return self.cur.fetchall()[:][0]

    def __check_db(self, file):
        if not os.path.isfile(file):
            with open(os.path.join(os.path.dirname(__file__), 'create.sql'), 'r') as f:
                sqlFile = f.read()

            sqlCommands = sqlFile.split(';')
            conn = sqlite3.connect(file)
            c = conn.cursor()
            for command in sqlCommands:
                c.execute(command)
            conn.close()

    def __del__(self):
        self.con.close()
