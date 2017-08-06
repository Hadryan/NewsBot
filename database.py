#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os


class Database():
    def __init__(self):
        self.con = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'data.db'))
        self.cur = self.con.cursor()

    def insert_news(self, title, text, link, img, site):
        self.cur.execute("INSERT INTO news (title, text, link, img_link, site_id) VALUES(%s, %s, %s, %s, "
                         + "(SELECT id FROM sites WHERE name=%s)')", (title, text, link, img, site))
        self.con.commit()

    def __del__(self):
        self.con.close()
