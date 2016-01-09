#!usr/bin/env python
# coding=UTF-8

import requests
import re
import json
from lxml import html
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class DoubanBookSpider(object):
	def __init__(self):
		self.s = requests.Session()
		self.header = {
            'Host': 'www.douban.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKi \
                    t/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
            'Cache-Control': 'max-age=0',
        }

	def