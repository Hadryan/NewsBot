#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests


def main():
    base_url = 'http://www.brohltal-info24.de/'
    response = requests.get(base_url + 'index.php?site=news-direkt').text
    data = re.findall('img src="([^"]*)".*\r\n.*\r\n.*\r\n[ ]*(.*?)[ ]*<.*?<br>[ \r\n]*(.*) <a href=([^>]*)', response)
    print(data)
    print(len(data))


if __name__ == '__main__':
    main()
