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

    def check_site(self, name, link):
        self.cur.execute("SELECT id FROM sites WHERE name=?", (name,))
        if len(self.cur.fetchall()) < 1:
            self._insert_site(name, link)

    def _insert_site(self, name, link):
        self.cur.execute("INSERT INTO sites (name, link) VALUES(?, ?)", (name, link))
        self.con.commit()

    def insert_news(self, title, text, link, img, site):
        self.cur.execute("INSERT INTO news (title, text, link, img_link, site_id) VALUES(?, ?, ?, ?, "
                         + "(SELECT id FROM sites WHERE name=?)')", (title, text, link, img, site))
        self.con.commit()

    def __check_db(self, file):
        if not os.path.isfile(file):
            fd = open(file, 'r')
            sqlFile = fd.read()
            fd.close()

            sqlCommands = sqlFile.split(';')
            conn = sqlite3.connect(file)
            c = conn.cursor()
            for command in sqlCommands:
                c.execute(command)
            conn.close()

    def __del__(self):
        self.con.close()
